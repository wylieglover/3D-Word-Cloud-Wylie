from sqlalchemy import Column, String, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime, timezone
import uuid

class AnalyzedArticle(Base):
    __tablename__ = "analyzed_articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    user = relationship("User", back_populates="articles")
    words = relationship("WordWeight", back_populates="article")

class WordWeight(Base):
    __tablename__ = "word_weights"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article_id = Column(UUID(as_uuid=True), ForeignKey("analyzed_articles.id"), nullable=False)
    word = Column(String, nullable=False)
    weight = Column(Float, nullable=False)
    article = relationship("AnalyzedArticle", back_populates="words")
