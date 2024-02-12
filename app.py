import json
from flask import Flask,render_template,request,flash,session,g,url_for,redirect
import requests
from google.cloud import storage
import os
from flask_googlestorage import GoogleStorage, Bucket
app = Flask(__name__,template_folder='templates')

app.config['SECRET_KEY'] = 'secret-key-goes-here'

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist("files")
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'aniruddho-chatterjee-fall2023-acb87efd5ca0.json'
        client = storage.Client(project='aniruddho-chatterjee-fall2023')
        bucket = client.get_bucket('books-dataset')
        for file in files:
            blob = bucket.blob(file.filename)
            blob.upload_from_file(file,content_type='text/plain')
            flash(f'File {file.filename} uploaded successfully!', 'success')
    if request.method == 'POST':
        return render_template('index.html')
    else:
        return render_template('upload.html')

@app.route('/search/<string:inputText>', methods=['GET','POST'])
def search(inputText):
    cnt = ""
    params = {"keyword":inputText.lower()}
    url = "https://us-central1-aniruddho-chatterjee-fall2023.cloudfunctions.net/search"
    response = requests.post(url = url,json=params)
    if response.status_code == 200:
        return render_template('search.html',response=json.loads(response.content))
    else:
        flash('Keyword Not Found', 'error')
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)