from app import db
from datetime import datetime


class Dump(db.Model):
    __tablename__ = "dumps"

    md5 = db.Column(db.String(32), primary_key=True)
    file_path = db.Column(db.String(512), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    analysis_result = db.Column(db.JSON, nullable=False)


    def __repr__(self):
        return f"<FileDump md5={self.md5} path={self.file_path}>"