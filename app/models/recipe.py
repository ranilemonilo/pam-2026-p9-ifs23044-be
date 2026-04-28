from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime, timezone
from ..extensions import Base

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    ingredients = Column(Text)
    steps = Column(Text)
    category = Column(String(100))
    difficulty = Column(String(50))
    duration_minutes = Column(Integer)
    request_id = Column(Integer, ForeignKey("requests.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))