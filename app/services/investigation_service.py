from models.investigation import Investigation
from models.user import User
from app import db
import os

# -----------------------------
# Tutte le investigations
# -----------------------------
def get_all():
    """Restituisce tutte le investigations presenti nel DB"""
    return Investigation.query.all()


# -----------------------------
# Singola investigation per ID
# -----------------------------
def get_by_id(inv_id):
    """Restituisce una singola investigation per ID"""
    return Investigation.query.get(inv_id)


# -----------------------------
# Creazione di una nuova investigation
# -----------------------------
def create(data, file_path):
    """
    data: dict con 'name' e 'emails' (stringa separata da virgola)
    file_path: path al dump file
    """
    name = data.get("name")
    emails_str = data.get("emails")

    if not name or not emails_str:
        raise ValueError("Dati incompleti per la creazione dell'investigation")

    # Trasforma la stringa in lista di email
    email_list = [email.strip() for email in emails_str.split(",") if email.strip()]


    # Trova gli utenti nel DB
    users = User.query.filter(User.email.in_(email_list)).all()
    if not users:
        raise ValueError("Nessun utente trovato con queste email")

    # Crea l'investigation e associa gli utenti
    inv = Investigation(
        name=name,
        dump_path=file_path,
        users=users
    )

    db.session.add(inv)
    db.session.commit()
    return inv


# -----------------------------
# Aggiornamento investigation esistente
# -----------------------------
def update(inv_id, data, file_path=None):
    inv = get_by_id(inv_id)
    if not inv:
        raise ValueError("Investigation non trovata")

    # Aggiorna nome
    inv.name = data.get("name", inv.name)

    # Aggiorna gli utenti se forniti
    emails_str = data.get("emails")
    if emails_str:
        email_list = [email.strip() for email in emails_str.split(",") if email.strip()]
        users = User.query.filter(User.email.in_(email_list)).all()
        inv.users = users  # aggiorna associazioni many-to-many

    # Aggiorna dump file se fornito
    if file_path:
        inv.dump_path = file_path

    db.session.commit()
    return inv


# -----------------------------
# Eliminazione investigation
# -----------------------------
def delete(inv_id):
    inv = get_by_id(inv_id)
    if not inv:
        raise ValueError("Investigation non trovata")

    db.session.delete(inv)
    db.session.commit()


# -----------------------------
# Restituisce tutte le investigations accessibili da un utente
# -----------------------------
def get_all_by_user_email(user_email):
    """
    Restituisce le investigations a cui l'utente ha accesso
    """
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return []

    # SQLAlchemy gestisce la relazione many-to-many
    return user.investigations


# -----------------------------
# Placeholder analisi dump TODO
# -----------------------------
def execute_analysis(inv_id):
    """
    Analizza il dump dell'investigation (da implementare)
    """
    inv = get_by_id(inv_id)
    if not inv:
        raise ValueError("Investigation non trovata")

    # TODO: implementare l'analisi tramite Volatility sul file inv.dump_path
    pass