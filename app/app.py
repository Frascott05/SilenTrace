import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'db.sqlite3')

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "super-secret-key")
app.config['JWT_EXPIRATION_HOURS'] = int(os.environ.get("JWT_EXPIRATION_HOURS", 24))

app.config["VOLATILITY_PATH"] = os.getenv("VOLATILITY_PATH")

db = SQLAlchemy(app)

# MODELS
from models.investigation import Investigation
from models.user import User
from models.dumps import Dump

# BLUEPRINTS
from routes.main import main_bp
from routes.investigation import investigation_bp
from routes.auth import auth_bp
from routes.admin import admin_bp

app.register_blueprint(main_bp)
app.register_blueprint(investigation_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

# 👉 POI init DB
with app.app_context():
    print("Creating DB...")
    db.create_all()
    
    print("Clearing Dump table...")
    db.session.query(Dump).delete()
    db.session.commit()

    print("Tables:", db.metadata.tables.keys())