from flask import current_app

from models.investigation import Investigation
from models.user import User
from models.dumps import Dump
from app import db
import os

from services.volatilityServices.VolatilityBatchRunner import VolatilityBatchRunner
from services.enums.VolatilityPlugins import VolatilityPlugins
from services.enums.OperativeSystems import OperativeSystems

from utils import hash

# -----------------------------
# All the investigations
# -----------------------------
def get_all():
    """
    :return List of Investigation:  All the investigation in the DB"""
    return Investigation.query.all()


# -----------------------------
# Single investigation found by ID
# -----------------------------
def get_by_id(inv_id):
    """
    :return Investigation: investigation with the given ID
    """
    return Investigation.query.get(inv_id)


# -----------------------------
# Creation of a new investigation
# -----------------------------
def create(data, file_path):
    """
    :param data: Dictionary with 'name' and 'emails'
    :param file_path: path to dump file
    :return Investigation: returns the investigation created
    """
    name = data.get("name")
    emails_str = data.get("emails")

    if not name or not emails_str:
        raise ValueError("Incomplete data for creating the investigation")

    # Converting email string into a list of emails
    email_list = [email.strip() for email in emails_str.split(",") if email.strip()]


    # Looking for users in DB
    users = User.query.filter(User.email.in_(email_list)).all()
    if not users:
        raise ValueError("No user found with this email")

    # Create the investigation
    inv = Investigation(
        name=name,
        dump_path=file_path,
        users=users
    )

    db.session.add(inv)
    db.session.commit()
    return inv


# -----------------------------
# Updating an existing investigation 
# -----------------------------
def update(inv_id, data, file_path=None):
    """
    :param inv_id: Investigation ID
    :param data: Dictionary with 'name' and 'emails'
    :param file_path: path to dump file (Default None)
    :return Investigation: returns the updated investigation
    """
    inv = get_by_id(inv_id)
    if not inv:
        raise ValueError("Investigation not found")

    inv.name = data.get("name", inv.name)

    emails_str = data.get("emails")
    if emails_str:
        email_list = [email.strip() for email in emails_str.split(",") if email.strip()]
        users = User.query.filter(User.email.in_(email_list)).all()
        inv.users = users

    if file_path:
        inv.dump_path = file_path

    db.session.commit()
    return inv


# -----------------------------
# Delete investigation
# -----------------------------
def delete(inv_id):
    """
    :param inv_id: investigation id
    """
    inv = get_by_id(inv_id)
    if not inv:
        raise ValueError("Investigation non trovata")

    db.session.delete(inv)
    db.session.commit()


# -----------------------------
# All the investigation accessible by user
# -----------------------------
def get_all_by_user_email(user_email):
    """
    :param user_email: the user email to check
    :return List[Investigation]: with all the users investigation
    :return []: if user is not provvided
    """
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return []

    return user.investigations


# -----------------------------
# Dump Analysis
# -----------------------------
def execute_analysis(inv, plugins=None):
    """
    Analyze the dump and gives the analysis result as a JSON
    
    :param inv: investigation
    :param plugins: list of plugins to execute, if None it uses all the pre-loaded plugins
    """
    if not inv:
        raise ValueError("Investigation not found")

    dump_path = inv.dump_path

    if not dump_path or not os.path.exists(dump_path):
        raise ValueError("Dump file not found for this investigation")

    print("Calculating hash")
    # 🔐 1. Calculating Hash
    hashing = hash.FileHashCalculator(dump_path).calculate_hashes()
    md5_hash = hashing.get("md5")
    print(md5_hash)

    if not md5_hash:
        raise ValueError("Errore in MD5 calculus")

    # 🔍 2. Lookup in DB
    existing_dump = Dump.query.filter_by(md5=md5_hash).first()

    if existing_dump:
        current_app.logger.info(f"[CACHE HIT] Dump already analyzed: {md5_hash}")
        return existing_dump.analysis_result, hashing

    current_app.logger.info(f"[CACHE MISS] New Dump: {md5_hash}")

    # ⚙️ 3. Plugin selection
    if plugins is None:
        plugins = [p.value for p in VolatilityPlugins]

    # 🧠 4. Execution
    runner = VolatilityBatchRunner(
        current_app.config["VOLATILITY_PATH"],
        dump_path,
        plugins,
        OperativeSystems.DEFAULT
    )

    #this is a warmup to avoid the first plugin to crash for finding debug sybols
    warmup = runner._run_single_plugin("info", json=False)

    runner.run_all(True)
    results = runner.get_all_result()

    # 💾 5. Save into DB
    try:
        new_dump = Dump(
            md5=md5_hash,
            file_path=dump_path,
            analysis_result=results
        )

        db.session.add(new_dump)
        db.session.commit()

        current_app.logger.info(f"[DB SAVE] Dump saved: {md5_hash}")

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"[DB ERROR] Error while storing dump: {str(e)}")

    return results, hashing