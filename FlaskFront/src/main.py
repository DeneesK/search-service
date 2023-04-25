import requests
from flask import Flask, render_template, request


app = Flask(import_name='front')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        req = request.form.to_dict()
        resp = requests.post('http://auth:8000/user/get-token', json=req).json()
        print(resp)


@app.route('/search/')
def send_query():
    query = request.values.get('query')
    resp = requests.get(f'http://search:8000/api/v1/search?query={query}').json()
    return render_template('search.html', resp=resp)


@app.route('/reg/', methods=['GET', 'POST'])
def create_user():
    if request.method == 'GET':
        return render_template('reg.html')
    elif request.method == 'POST':
        req = request.form.to_dict()
        resp = requests.post('http://auth:8000/user/registration', json=req).json()
        print(resp)
        return render_template('index.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
