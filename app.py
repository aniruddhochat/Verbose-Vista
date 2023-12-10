import json

from flask import Flask,render_template,request,flash,session,g,url_for,redirect
import requests
app = Flask(__name__,template_folder='templates')

app.config['SECRET_KEY'] = 'secret-key-goes-here'

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/search/<string:inputText>', methods=['GET','POST'])
def search(inputText):
    params = {"keyword":inputText}
    url = "https://us-central1-aniruddho-chatterjee-fall2023.cloudfunctions.net/search"
    response = requests.post(url = url,json=params)
    return render_template('search.html',response=json.loads(response.content))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')