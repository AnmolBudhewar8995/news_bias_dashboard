# src/nlp_pipeline.py
from transformers import pipeline
from textblob import TextBlob
import numpy as np
from sentence_transformers import SentenceTransformer
import ast

sent_pipe = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

EMOTIVE_WORDS = set([
    "outrage","shocking","crisis","emergency","devastating","scandal","controversial",
    "celebrate","delighted","thrilled","disaster","tragic","alarm"
])

def compute_sentiment(text):
    try:
        r = sent_pipe(text[:512])  # limit length for speed
        label = r[0]['label']
        score = r[0]['score']
        val = score if label == "POSITIVE" else -score
        return float(val)
    except Exception:
        return None

def compute_subjectivity(text):
    try:
        tb = TextBlob(text[:2000])
        return float(tb.sentiment.subjectivity)
    except Exception:
        return None

def emotive_ratio(text):
    t = text.lower()
    words = t.split()
    if not words:
        return 0.0
    emotive_count = sum(1 for w in words if w in EMOTIVE_WORDS)
    return emotive_count / len(words)

def compute_embedding(text):
    emb = embed_model.encode(text, convert_to_numpy=True)
    return emb.tolist()

# helpers to store/load embedding string form
def emb_to_str(emb):
    return ",".join(map(str, emb))


def str_to_emb(s):
    if not s:
        return None
    return np.array(list(map(float, s.split(","))))

def calculate_bias(text, sentiment, subjectivity):
    """
    Calculate bias score based on text content, sentiment, and subjectivity.
    Higher absolute values indicate more potential bias.
    """
    try:
        # Basic bias calculation combining sentiment and subjectivity
        # Positive sentiment with high subjectivity might indicate emotional framing
        # Negative sentiment with high subjectivity might indicate negative framing
        
        if sentiment is None or subjectivity is None:
            return 0.0
            
        # Combine sentiment and subjectivity for bias score
        # Subjectivity amplifies the sentiment signal
        bias_score = sentiment * (1 + subjectivity)
        
        # Add some text-based analysis for additional bias detection
        text_lower = text.lower()
        
        # Check for biased language patterns
        biased_terms = [
            'shocking', 'outrageous', 'scandal', 'crisis', 'disaster',
            'amazing', 'incredible', 'miracle', 'breakthrough', 'victory'
        ]
        
        bias_multiplier = 1.0
        for term in biased_terms:
            if term in text_lower:
                bias_multiplier += 0.1
                
        final_bias = bias_score * bias_multiplier
        
        # Clamp to reasonable range
        return max(-5.0, min(5.0, final_bias))
        
    except Exception:
        return 0.0
