from app import app
from flask import render_template, request, redirect, url_for
from services import investigation_service as service
import os

UPLOAD_FOLDER = 'static/uploads'

@app.route('/')
def index():
    investigations = service.get_all()
    return render_template('index.html', investigations=investigations)

@app.route('/create', methods=['POST'])
def create():
    file = request.files['file']
    path = None
    if file:
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

    service.create(request.form, path)
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    file = request.files.get('file')
    path = None
    if file and file.filename:
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

    service.update(id, request.form, path)
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    service.delete(id)
    return redirect(url_for('index'))

@app.route('/investigation/<int:id>')
def view(id):
    inv = service.get_by_id(id)
    return render_template('investigation.html', investigation=inv)