# src/bias_scoring.py
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from src.db import list_articles, update_article_features
from src.nlp_pipeline import str_to_emb, emb_to_str
from sqlalchemy import create_engine
from collections import defaultdict
import math

def cluster_topics(n_clusters=12):
    arts = list_articles(limit=1000)
    emb_list = []
    ids = []
    for a in arts:
        if a.embedding:
            emb = str_to_emb(a.embedding)
            emb_list.append(emb)
            ids.append(a.id)
    if not emb_list:
        print("No embeddings found to cluster.")
        return
    X = np.stack(emb_list)
    n_clusters = min(n_clusters, len(X))
    cl = AgglomerativeClustering(n_clusters=n_clusters).fit(X)
    labels = cl.labels_
    for idx, art_id in enumerate(ids):
        update_article_features(art_id, topic=int(labels[idx]))

def compute_relative_bias():
    # For each topic, compute per-source mean sentiment and global mean; bias = source_mean - topic_mean
    arts = list_articles(limit=2000)
    # group by topic and source
    grouped = {}
    topics = defaultdict(list)
    for a in arts:
        topic = a.topic if a.topic is not None else -1
        topics[topic].append(a)
    for topic, items in topics.items():
        # compute mean sentiment across all sources
        vals = [it.sentiment for it in items if it.sentiment is not None]
        if not vals:
            continue
        topic_mean = float(np.mean(vals))
        # per source
        by_source = {}
        for it in items:
            if it.sentiment is None:
                continue
            by_source.setdefault(it.source, []).append(it.sentiment)
        for src, svals in by_source.items():
            src_mean = float(np.mean(svals))
            bias = src_mean - topic_mean  # positive = more positive than peers on this topic
            # normalize by std of topic to scale
            topic_std = float(np.std(vals)) if len(vals)>1 else 1.0
            bias_norm = bias / (topic_std+1e-6)
            # update each article of that source & topic with bias score
            for it in items:
                if it.source == src:
                    # combined bias metric: relative sentiment + framing (subjectivity*emotive)
                    framing = (it.subjectivity or 0.0) * (it.emotive_score or 0.0)
                    combined = 0.6 * bias_norm + 0.4 * framing
                    # clamp
                    combined = max(-5, min(5, combined))
                    update_article_features(it.id, bias_score=float(combined))
