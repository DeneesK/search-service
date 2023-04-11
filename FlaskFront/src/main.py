from flask import Flask, render_template


app = Flask(import_name='front')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
