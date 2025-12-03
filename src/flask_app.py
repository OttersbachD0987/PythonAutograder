import os
import json
from flask import Flask, render_template, g, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from autograder.autograder_application import Autograder
from autograder.project_settings import Requirement
from autograder.code_test_type import IParameterGroup, ParameterRepresentation
from autograder.code_test import CodeTest, DictionaryTestNode, LiteralTestNode, ProjectTestNode, CodeTestNode
from typing import Any, cast

UPLOAD_FOLDER = os.path.join(os.curdir, 'static/temp')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_CONFIG_EXTENSIONS = {'json'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app = Flask(__name__)
var = 3
grader: Autograder = Autograder()
grader.loadConfiguration("Configurations/config.json")

grader.extension_manager.loadFromDirectory("./Extensions")
grader.extension_manager.importExtensions()

context: str = ""
testsToRun: list[str] = []

data: dict[str, Any] = {
    "autograder": grader
}

bog = {}

instructor = ""
students = []

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'

def allowed_config_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_CONFIG_EXTENSIONS

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_py_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ["py"]


@app.route("/upload_config", methods=['GET', 'POST'])
def upload_config():
    global grader
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return {"message": "No file part"}
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return {"message": "No selected file"}
        if file and allowed_config_file(file.filename):
            filename = secure_filename(file.filename)
            jsoning = json.load(file.stream)
            print(jsoning)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            grader.setConfigurationFromDict(jsoning)
            return jsoning
    return {"message": "Wrong method?"}

@app.route("/upload_instructor", methods=['GET', 'POST'])
def upload_instructor():
    global instructor
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return {"message": "No file part"}
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return {"message": "No selected file"}
        if file and allowed_py_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            instructor = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            return {"filepath": instructor}
    return {"message": "Wrong method?"}

@app.route("/upload_students", methods=['GET', 'POST'])
def upload_students():
    global students
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return {"message": "No file part"}
        files = request.files.getlist("file")
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        paths = []
        for file in files:
            if file.filename == '':
                flash('No selected file')
                return {"message": "No selected file"}
            if file and allowed_py_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                students.append(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return students
    return {"message": "Wrong method?"}

@app.route("/upload_tests_config", methods=['GET', 'POST'])
def upload_tests_config() -> dict[str, str] | Any:
    global bog
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return {"message": "No file part"}
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return {"message": "No selected file"}
        if file and allowed_config_file(file.filename):
            filename = secure_filename(file.filename)
            jsoning = json.load(file.stream)
            print(jsoning)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            bog = jsoning
            return jsoning
    return {"message": "Wrong method?"}

@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return {"message": "No file part"}
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return {"message": "No selected file"}
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return {"message": "Success", "filepath": os.path.join(app.config['UPLOAD_FOLDER'], filename)}
    return {"message": "Wrong method?"}

@app.route("/", methods=['GET', 'POST'])
def hello_world():

    return render_template('base.html')

@app.route("/me")
def me_api():
    global var
    var += 1
    return {
        "username": var
    }

if __name__ == "__main__":
    print("We are starting.")
    app.run()
    print("We are done.")