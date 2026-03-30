from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import text
from models.user import User
from app import db
from utils.middelware import jwt_required

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")

@admin_bp.route("/", methods=["GET", "POST"])
@jwt_required
def admin_panel(user):
    # Gain access to the current user's email from the JWT token
    current_user_identity = user.email
    user = User.query.filter_by(email=current_user_identity).first()

    # Access control: only allow users with is_admin=True to access this route
    """if not user or not user.is_admin:
        flash("Access denied: only admins can access this panel", "danger")
        return redirect(url_for("Login.html"))"""

    result = None
    error = None

    if request.method == "POST":
        query = request.form.get("query")
        if query:
            try:
                # Use sqlalchemy.text() for a raw query
                result = db.session.execute(text(query))
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                error = str(e)

    return render_template("admin_panel.html", result=result, error=error)