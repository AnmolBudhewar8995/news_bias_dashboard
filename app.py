# app.py

import streamlit as st
from src.db import list_articles, init_db
import pandas as pd
import plotly.express as px
from datetime import datetime

# Initialize database before any queries
init_db()

st.set_page_config(layout="wide", page_title="Local News Sentiment & Bias Dashboard")
st.title("Local News Sentiment & Bias Dashboard")

st.sidebar.header("Actions")
if st.sidebar.button("Fetch & analyze now"):
    import src.run_pipeline as rp
    rp.run_all()
    st.success("Fetched and processed feeds.")



# load recent articles
try:
    arts = list_articles(limit=1000)
except Exception as e:
    st.error(f"Database error: {e}")
    st.info("Database not initialized. Click 'Fetch & analyze now' to initialize and collect articles.")
    st.stop()

# Check if we have articles
if not arts or len(arts) == 0:
    st.info("No articles yet. Click 'Fetch & analyze now' to collect articles.")
    st.stop()


# convert to DataFrame
rows = []
for a in arts:
    rows.append({
        "id": a.id,
        "source": a.source,
        "title": a.title,
        "published": a.published,
        "sentiment": a.sentiment,
        "subjectivity": a.subjectivity,
        "emotive": a.emotive_score,
        "topic": a.topic,
        "bias_score": a.bias_score
    })

# Create DataFrame with proper columns even if empty
columns = ["id", "source", "title", "published", "sentiment", "subjectivity", "emotive", "topic", "bias_score"]
df = pd.DataFrame(rows, columns=columns)

# Check if we have any data
if len(rows) == 0:
    st.info("No articles yet. Click 'Fetch & analyze now' to collect articles.")
    st.stop()

sources = sorted(df['source'].dropna().unique().tolist())
selected_sources = st.sidebar.multiselect("Sources", sources, default=sources)
topic_vals = sorted(df['topic'].dropna().unique().tolist())
selected_topics = st.sidebar.multiselect("Topics", topic_vals, default=topic_vals)

# filtered DataFrame
dff = df[df['source'].isin(selected_sources) & df['topic'].isin(selected_topics)]

st.header("Overview")
col1, col2 = st.columns(2)
with col1:

    fig = px.line(dff.groupby(pd.to_datetime(dff['published']).dt.date)['sentiment'].mean().reset_index().rename(columns={"published":"date","sentiment":"avg_sentiment"}),
                  x='date', y='avg_sentiment', title="Avg sentiment over time")
    st.plotly_chart(fig, width='stretch')
with col2:
    fig2 = px.box(dff, x='source', y='bias_score', title="Bias score distribution by source")
    st.plotly_chart(fig2, width='stretch')

st.subheader("Top flagged articles (high absolute bias)")
top = dff.reindex(dff['bias_score'].abs().sort_values(ascending=False).index).head(20)
st.dataframe(top[['published','source','title','sentiment','subjectivity','emotive','bias_score']], height=400)

st.subheader("Per-topic sentiment comparison")
topic = st.selectbox("Choose topic", sorted(dff['topic'].dropna().unique().tolist()))
if topic is not None:
    dtopic = dff[dff['topic']==topic]
    fig3 = px.bar(dtopic.groupby('source')['sentiment'].mean().reset_index(), x='source', y='sentiment', title=f"Avg sentiment for topic {topic}")
    st.plotly_chart(fig3, use_container_width=True)


st.subheader("Article viewer")
# Handle NaN values in id column
valid_ids = dff['id'].dropna().astype(int)
if len(valid_ids) > 0:
    sel_id = st.number_input("Enter article id", min_value=int(valid_ids.min()), max_value=int(valid_ids.max()), value=int(valid_ids.min()))
    art = next((a for a in arts if a.id == sel_id), None)
    if art:
        st.markdown(f"**{art.title}**  — *{art.source}*  — {art.published}")
        st.write(art.text[:10000])
        st.write(f"Sentiment: {art.sentiment}  | Subjectivity: {art.subjectivity} | Emotive ratio: {art.emotive_score} | Bias score: {art.bias_score}")
else:
    st.info("No valid article IDs found.")
