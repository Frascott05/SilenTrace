from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import text
from models.user import User
from app import db
from utils.middelware import jwt_required

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")

@admin_bp.route("/", methods=["GET", "POST"])
@jwt_required
def admin_panel(user):
    # Ottieni l'utente corrente
    current_user_identity = user.email
    user = User.query.filter_by(email=current_user_identity).first()

    # Controllo admin (decommenta se vuoi abilitare)
    #test@test pwd: test as default admin user
    if not user or not user.is_admin:
        flash("Accesso negato: solo admin", "danger")
        return redirect(url_for("main.index"))

    result = None
    error = None

    if request.method == "POST":
        query = request.form.get("query")
        if query:
            try:
                # Usa sqlalchemy.text() per query raw
                result = db.session.execute(text(query))
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                error = str(e)

    return render_template("admin_panel.html", result=result, error=error)