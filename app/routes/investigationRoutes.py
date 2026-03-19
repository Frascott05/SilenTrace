from app import app
from flask import render_template, request, redirect, url_for
from services import investigation_service as service
import os

UPLOAD_FOLDER = 'static/uploads'

@app.route('/investigations/', methods=['GET'])
def InvestigationList():
    investigations = service.get_all()
    return render_template('index.html', investigations=investigations)

@app.route('/investigation/create', methods=['POST'])
def create():
    file = request.form.get('filename') 
    path = path = os.path.abspath(os.path.join('app', 'dumps', file))

    # maybe in future you can implement the file upload
    # if file and file:
    #     path = os.path.join(UPLOAD_FOLDER, file)
    #     file.save(path)

    service.create(request.form, path)
    return redirect(url_for('investigations'))

@app.route('/investigation/update/<int:id>', methods=['POST'])
def update(id):
    file = request.form.get('filename') 
    path = path = os.path.abspath(os.path.join('app', 'dumps', file))
    # maybe in future you can implement the file upload
    # if file and file:
    #     path = os.path.join(UPLOAD_FOLDER, file)
    #     file.save(path)

    service.update(id, request.form, path)
    return redirect(url_for('investigations'))

@app.route('/investigation/delete/<int:id>')
def delete(id):
    service.delete(id)
    return redirect(url_for('investigations'))

@app.route('/investigation/<int:id>', methods=['GET'])
def view(id):

    ##call the services
    inv = service.get_by_id(id)
    return render_template('investigation.html', investigation=inv)