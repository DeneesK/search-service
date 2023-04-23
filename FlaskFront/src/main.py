import requests
from flask import Flask, render_template, request


app = Flask(import_name='front')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search/')
def send_query():
    query = request.values.get('query')
    r = requests.get(f'http://search:8000/api/v1/search?query={query}')
    print(query)
    resp = r.json()
    return render_template('search.html', resp=resp)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
