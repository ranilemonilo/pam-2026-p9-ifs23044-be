from datetime import datetime
from app.utils.extensions import db

class RequestLog(db.Model):
    __tablename__ = "request_logs"

    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(200), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    status_code = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "endpoint": self.endpoint,
            "method": self.method,
            "status_code": self.status_code,
            "created_at": self.created_at.isoformat(),
        }