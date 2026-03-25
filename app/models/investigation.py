from app import db
from datetime import datetime

# --- Tabella di associazione ---
investigation_users = db.Table(
    "investigation_users",
    db.Column("investigation_id", db.Integer, db.ForeignKey("investigations.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"))
)

# --- Modello Investigation ---
class Investigation(db.Model):
    __tablename__ = "investigations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    dump_path = db.Column(db.String(500), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relazione con utenti
    users = db.relationship(
        "User",
        secondary=investigation_users,
        backref="investigations"
    )

    def __repr__(self):
        return f"<Investigation {self.name}>"