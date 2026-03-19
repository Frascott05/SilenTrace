from models.investigation import Investigation
from app import db

def get_all():
    return Investigation.query.all()

def get_by_id(id):
    return Investigation.query.get(id)

def create(data, file_path):
    inv = Investigation(
        name=data['name'],
        emails=data['emails'],
        dump_file=file_path
    )
    db.session.add(inv)
    db.session.commit()

def update(id, data, file_path=None):
    inv = Investigation.query.get(id)
    inv.name = data['name']
    inv.emails = data['emails']
    if file_path:
        inv.dump_file = file_path
    db.session.commit()

def delete(id):
    inv = Investigation.query.get(id)
    db.session.delete(inv)
    db.session.commit()

def executeAnalisys():
    #implement here the analisys of the investigation dump via volatility
    pass