import os
from flask import Flask, render_template, g, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(os.curdir, 'static/temp')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
var = 3

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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