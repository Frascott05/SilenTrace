from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import current_app
from services import investigation_service as service
from utils.middelware import jwt_required
import os

investigation_bp = Blueprint("investigation", __name__, url_prefix="/api/investigation")

def get_upload_dir():
    return os.path.join(current_app.root_path, "static/uploads")

# -----------------------------
# List investigations (DEFAULT: only the ones for the logged user)
# -----------------------------
@investigation_bp.route("/investigations/")
@jwt_required
def list(user):
    investigations = service.get_all_by_user_email(user.email)

    #if you want to give all the user the possibility to view all the investigation use this instead
    #investigations = service.get_all()

    print(investigations)
    return render_template("index.html", investigations=investigations, user_email=user.email)


# -----------------------------
# Investigation Creation
# -----------------------------
@investigation_bp.route("/create", methods=["POST"])
@jwt_required
def create(user):
    
    name = request.form.get("name")
    emails_str = request.form.get("emails")
    file = request.form.get("filename")

    if not name or not emails_str:
        flash("Some required data are missing")
        return redirect(url_for("investigation.list"))


    if not file:
        raise ValueError("Missing dump file")

    filename = os.path.basename(file)
    path = os.path.join(get_upload_dir(), filename)
    print(path)

    try:
        service.create(request.form.to_dict(), path)
        flash("Investigation successful created")
    except ValueError as e:
        print("ERRORE CREATE:", e)
        flash(str(e))

    return redirect(url_for("investigation.list"))


# -----------------------------
# Investigation Update
# -----------------------------
@investigation_bp.route("/update/<int:id>", methods=["POST"])
@jwt_required
def update(user, id):
    inv = service.get_by_id(id)
    if not inv:
        flash("Investigation not found")
        return redirect(url_for("investigation.list"))

    # Permits control
    if user.email not in [u.email for u in inv.users]:
        flash("You don't have the right permits to update this investigation")
        return redirect(url_for("investigation.list"))

    #Update process
    name = request.form.get("name")
    file = request.form.get("filename")
    path = os.path.join(get_upload_dir(), file) if file else None

    service.update(id, request.form, path)
    flash("Investigation updated")
    return redirect(url_for("investigation.list", id=id))


# -----------------------------
# Investigation Delete
# -----------------------------
@investigation_bp.route("/delete/<int:id>", methods=["POST"])
@jwt_required
def delete(user, id):
    inv = service.get_by_id(id)
    if not inv:
        flash("Investigation not found")
        return redirect(url_for("investigation.list"))

    # Access Control
    if user.email not in [u.email for u in inv.users]:
        flash("You don't have the right permits to delete this investigation")
        return redirect(url_for("investigation.list"))

    service.delete(id)
    flash("Investigation deleted")
    return redirect(url_for("investigation.list"))


# -----------------------------
# Details of a specified investigation
# -----------------------------
@investigation_bp.route("/details/<int:id>")
@jwt_required
def view(user, id):
    inv = service.get_by_id(id)
    if not inv:
        flash("Investigation not found")
        return redirect(url_for("investigation.list"))

    # Access control
    if user.email not in [u.email for u in inv.users]:
        flash("You don't have the right permits to view this investigation")
        return redirect(url_for("investigation.list"))

    #Execution of the dump analysis and getting the results as json
    try:
        analysis_json, hashing = service.execute_analysis(inv) #TODO IMPLEMENT ASYNC FOR PRODUCTION PURPOSES (CELERY/ASYNC JOBS)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("investigation.list"))

    return render_template("investigation.html", investigation=inv, analysis=analysis_json, hashes = hashing)