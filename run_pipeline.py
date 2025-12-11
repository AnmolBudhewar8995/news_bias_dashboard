# src/run_pipeline.py
from src.db import list_articles, update_article_features

from src.nlp_pipeline import compute_sentiment, compute_subjectivity, emotive_ratio, compute_embedding, emb_to_str, calculate_bias
from src.fetcher import fetch_and_store
from src.bias_scoring import cluster_topics, compute_relative_bias

def run_all():
    print("Fetching feeds...")
    fetch_and_store()
    print("Computing NLP features for new articles...")
    arts = list_articles(limit=5000)

    for a in arts:
        # compute only if no features
        if a.sentiment is None:
            s = compute_sentiment(a.text)
            subj = compute_subjectivity(a.text)
            emot = emotive_ratio(a.text)
            emb = compute_embedding(a.text[:1000])
            bias = calculate_bias(a.text, s, subj)
            update_article_features(a.id, sentiment=s, subjectivity=subj, emotive_score=emot, embedding=",".join(map(str, emb)), bias_score=bias)
    print("Clustering topics...")
    cluster_topics(n_clusters=12)
    print("Computing relative bias...")
    compute_relative_bias()
    print("Done pipeline.")
