from flask import Flask, request, jsonify
import os
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER,exit_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

