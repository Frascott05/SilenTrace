from app import app, db
##to review
with app.app_context():
    db.create_all()