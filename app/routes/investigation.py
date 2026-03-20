from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import current_app
from services import investigation_service as service
from utils.middelware import jwt_required  # il tuo decoratore
import os

investigation_bp = Blueprint("investigation", __name__, url_prefix="/api/investigation")

def get_upload_dir():
    return os.path.join(current_app.root_path, "dumps")

# -----------------------------
# Lista investigations (solo quelle accessibili all'utente)
# -----------------------------
@investigation_bp.route("/investigations/")
@jwt_required
def list(user):
    investigations = service.get_all_by_user_email(user.email)
    #investigations = service.get_all()
    print(investigations)
    return render_template("index.html", investigations=investigations)


# -----------------------------
# Creazione investigation
# -----------------------------
@investigation_bp.route("/create", methods=["POST"])
@jwt_required
def create(user):
    
    name = request.form.get("name")
    emails_str = request.form.get("emails")
    file = request.form.get("filename")

    #prova a commentare questa
    if not name or not emails_str:
        flash("Dati mancanti per creare l'investigation")
        return redirect(url_for("investigation.list"))

    path = os.path.join(get_upload_dir(), file)

    try:
        service.create(request.form.to_dict(), path)
        flash("Investigation creata con successo")
    except ValueError as e:
        print("ERRORE CREATE:", e)
        flash(str(e))

    return redirect(url_for("investigation.list"))


# -----------------------------
# Aggiornamento investigation
# -----------------------------
@investigation_bp.route("/update/<int:id>", methods=["POST"])
@jwt_required
def update(user, id):
    inv = service.get_by_id(id)
    if not inv:
        flash("Investigation non trovata")
        return redirect(url_for("investigation.list"))

    # Controllo accesso
    if user.email not in [u.email for u in inv.users]:
        flash("Non hai accesso per modificare questa investigation")
        return redirect(url_for("investigation.list"))

    # Procedi con l'update
    name = request.form.get("name")
    file = request.form.get("filename")
    path = os.path.join(get_upload_dir(), file) if file else None

    service.update(id, request.form, path)
    flash("Investigation aggiornata")
    return redirect(url_for("investigation.list", id=id))


# -----------------------------
# Eliminazione investigation
# -----------------------------
@investigation_bp.route("/delete/<int:id>", methods=["POST"])
@jwt_required
def delete(user, id):
    inv = service.get_by_id(id)
    if not inv:
        flash("Investigation non trovata")
        return redirect(url_for("investigation.list"))

    # Controllo accesso: solo utenti associati possono cancellare
    if user.email not in [u.email for u in inv.users]:
        flash("Non hai accesso per eliminare questa investigation")
        return redirect(url_for("investigation.list"))

    service.delete(id)
    flash("Investigation eliminata")
    return redirect(url_for("investigation.list"))


# -----------------------------
# Visualizzazione singola investigation
# -----------------------------
@investigation_bp.route("details/<int:id>")
@jwt_required
def view(user, id):
    inv = service.get_by_id(id)
    if not inv:
        flash("Investigation non trovata")
        return redirect(url_for("investigation.list"))

    # Controllo accesso utente
    if user.email not in [u.email for u in inv.users]:
        flash("Non hai accesso a questa investigation")
        return redirect(url_for("investigation.list"))

    return render_template("investigation.html", investigation=inv)