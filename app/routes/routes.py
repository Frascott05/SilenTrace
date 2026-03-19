from app import app
from flask import render_template, request, redirect, url_for
from services import investigation_service as service
import os

from routes.investigationRoutes import *

UPLOAD_FOLDER = 'static/uploads'

@app.route('/', methods=['GET'])
def index():
    investigations = service.get_all()
    return render_template('Home.html', investigations=investigations)
