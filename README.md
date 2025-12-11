# News Bias Dashboard

A comprehensive dashboard for analyzing sentiment, bias, and topic clustering in news articles. This application fetches news from multiple sources, processes them using advanced NLP techniques, and provides interactive visualizations to identify potential bias patterns.

![Dashboard Preview](https://via.placeholder.com/800x400?text=News+Bias+Dashboard+Preview)

## 🚀 Features

- **Real-time News Fetching**: Automatically fetches articles from configured RSS feeds
- **Advanced NLP Analysis**: 
  - Sentiment analysis using DistilBERT
  - Subjectivity scoring with TextBlob
  - Emotive language detection
  - Text embeddings for topic clustering
- **Bias Detection**: Multi-factor bias scoring algorithm
- **Interactive Visualizations**: 
  - Sentiment trends over time
  - Bias score distribution by source
  - Topic-based sentiment analysis
  - Article viewer with detailed metrics
- **Topic Clustering**: Automatic grouping of articles using embeddings
- **Relative Bias Analysis**: Compares sentiment patterns across sources and topics

## 📋 Requirements

- Python 3.8+
- Streamlit
- SQLAlchemy
- Pandas
- Plotly
- Transformers (Hugging Face)
- TextBlob
- Sentence Transformers
- Feedparser
- Newspaper3k
- Scikit-learn
- NumPy
- PyYAML

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd news_bias_dashboard
```

2. **Create a virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Install ML models (first run may take time):**
```bash
# Models will be downloaded automatically on first use:
# - distilbert-base-uncased-finetuned-sst-2-english (sentiment)
# - all-MiniLM-L6-v2 (embeddings)
```

## 🏃‍♂️ Quick Start

### 1. Configure News Sources

Edit `feeds.yaml` to add your preferred news sources:

```yaml
feeds:
  - name: "BBC News"
    url: "http://feeds.bbci.co.uk/news/rss.xml"
  - name: "Reuters"
    url: "https://feeds.reuters.com/reuters/topNews"
  - name: "Your Local News"
    url: "https://example-local-news.com/rss"
```

### 2. Run the Dashboard

```bash
streamlit run app.py
```

The dashboard will be available at `http://localhost:8501`

### 3. Fetch and Analyze Articles

1. Click "Fetch & analyze now" in the sidebar
2. Wait for the pipeline to complete (may take several minutes for first run)
3. Explore the interactive visualizations and analytics

## 📊 How It Works

### Pipeline Overview

1. **Data Collection**: Fetches articles from configured RSS feeds
2. **NLP Processing**: 
   - Sentiment analysis using transformer models
   - Subjectivity scoring
   - Emotive language detection
   - Text embedding generation
3. **Topic Clustering**: Groups similar articles using hierarchical clustering
4. **Bias Analysis**: 
   - Calculates relative bias compared to topic averages
   - Combines sentiment, subjectivity, and emotive language
   - Normalizes scores for comparison across sources
5. **Visualization**: Interactive charts and data tables

### Bias Scoring Algorithm

The bias score combines multiple factors:

```
bias_score = 0.6 × relative_sentiment_bias + 0.4 × framing_factor
```

Where:
- **Relative Sentiment Bias**: Source sentiment vs. topic average sentiment
- **Framing Factor**: Subjectivity × Emotive Language Ratio
- **Final Score**: Clamped between -5.0 and 5.0 for interpretability

### Metrics Explained

- **Sentiment**: Positive/Negative sentiment score (-1.0 to 1.0)
- **Subjectivity**: Objective vs. Subjective language (0.0 to 1.0)
- **Emotive Score**: Ratio of emotionally charged words
- **Bias Score**: Potential bias indicator (-5.0 to 5.0)
- **Topic**: Cluster ID for article grouping

## 📁 Project Structure

```
news_bias_dashboard/
├── app.py                 # Main Streamlit dashboard
├── src/
│   ├── db.py             # Database models and operations
│   ├── fetcher.py        # RSS feed fetching and parsing
│   ├── nlp_pipeline.py   # NLP processing functions
│   ├── bias_scoring.py   # Bias analysis algorithms
│   └── run_pipeline.py   # Main pipeline orchestration
├── feeds.yaml            # News source configuration
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🎯 Dashboard Sections

### Overview
- **Sentiment Timeline**: Average sentiment over time
- **Bias Distribution**: Box plots showing bias patterns by news source

### Top Flagged Articles
- Articles with highest absolute bias scores
- Sortable by various metrics

### Per-Topic Analysis
- Select specific topics for detailed analysis
- Compare sentiment across sources within topics

### Article Viewer
- Detailed view of individual articles
- Complete text and all computed metrics

## ⚙️ Configuration

### Database
- **Location**: `articles.db` (SQLite)
- **Auto-initialization**: Tables created automatically on first run

### Model Settings
- **Sentiment Model**: DistilBERT fine-tuned for sentiment analysis
- **Embedding Model**: Sentence-transformers all-MiniLM-L6-v2
- **Topic Clusters**: Default 12 clusters (configurable)

### Performance
- **Batch Processing**: Processes articles in batches for efficiency
- **Caching**: Model downloads cached for subsequent runs
- **Memory Management**: Processes text in chunks to manage memory usage

## 🔧 Troubleshooting

### Common Issues

1. **Database Errors**:
   ```bash
   # Delete database to start fresh
   rm articles.db
   ```

2. **Model Download Issues**:
   - Ensure stable internet connection for first run
   - Models are cached after download

3. **Memory Issues**:
   - Reduce batch size in `src/run_pipeline.py`
   - Process fewer articles at once

4. **RSS Feed Errors**:
   - Check feed URLs in `feeds.yaml`
   - Some feeds may be temporarily unavailable

### Debug Mode

Run with additional logging:
```bash
streamlit run app.py --logger.level debug
```

## 📈 Performance Considerations

- **First Run**: 5-15 minutes (model downloads + initial processing)
- **Subsequent Runs**: 1-5 minutes (depending on new articles)
- **Memory Usage**: ~2-4GB during processing
- **Storage**: Database grows with article count (~1MB per 100 articles)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Adding New Features

- **New NLP Models**: Modify `src/nlp_pipeline.py`
- **Additional Bias Factors**: Update `src/bias_scoring.py`
- **New Visualizations**: Add to `app.py`
- **Custom Data Sources**: Extend `src/fetcher.py`

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Hugging Face Transformers**: Pre-trained language models
- **Streamlit**: Interactive dashboard framework
- **TextBlob**: Sentiment analysis library
- **Sentence Transformers**: Embedding models

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Search existing issues
3. Create a new issue with detailed information

---

**Note**: This tool is for educational and research purposes. Bias detection is complex and this analysis should be considered alongside human editorial review and multiple analytical perspectives.
