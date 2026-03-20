from flask import Blueprint, render_template
from services import investigation_service as service

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    investigations = service.get_all()
    return render_template("Home.html", investigations=investigations)

@main_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("Login.html")

@main_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("Register.html")