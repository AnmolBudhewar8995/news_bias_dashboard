# src/db.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
from pathlib import Path

DB = Path("articles.db")
engine = create_engine(f"sqlite:///{DB}", connect_args={"check_same_thread": False})
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, index=True)
    source = Column(String)
    title = Column(String)
    published = Column(DateTime)
    text = Column(Text)
    sentiment = Column(Float, nullable=True)
    subjectivity = Column(Float, nullable=True)
    emotive_score = Column(Float, nullable=True)
    embedding = Column(Text, nullable=True)  # we store as stringified array for simplicity
    topic = Column(Integer, nullable=True)
    bias_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

def init_db():
    Base.metadata.create_all(engine)

def save_article_if_new(url, title, source, published, text):
    s = Session()
    ex = s.query(Article).filter(Article.url == url).first()
    if ex:
        s.close()
        return False
    art = Article(url=url, title=title, source=source, published=published, text=text)
    s.add(art)
    s.commit()
    s.close()
    return True

def list_articles(limit=200):
    s = Session()
    res = s.query(Article).order_by(Article.published.desc()).limit(limit).all()
    s.close()
    return res

def update_article_features(article_id, **kwargs):
    s = Session()
    art = s.query(Article).filter(Article.id == article_id).first()
    for k,v in kwargs.items():
        setattr(art, k, v)
    s.commit()
    s.close()
