from datetime import datetime
from app.utils.extensions import db

class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)   # JSON string
    steps = db.Column(db.Text, nullable=False)         # JSON string
    category = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        import json
        return {
            "id": self.id,
            "title": self.title,
            "ingredients": json.loads(self.ingredients),
            "steps": json.loads(self.steps),
            "category": self.category,
            "difficulty": self.difficulty,
            "duration_minutes": self.duration_minutes,
            "created_at": self.created_at.isoformat(),
        }