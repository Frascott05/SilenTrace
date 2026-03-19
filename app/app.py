import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'db.sqlite3')

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 👉 PRIMA modelli
from models.investigation import Investigation

# 👉 POI routes
from routes.routes import *

# 👉 POI init DB
with app.app_context():
    print("Creating DB...")
    db.create_all()
    print("Tables:", db.metadata.tables.keys())