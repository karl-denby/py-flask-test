from sys import version
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    header = "<h1>WSGI Works!!!</h1>"
    page = ""
    footer = ""
    return header + page + footer


@app.route('/test')
def test():
    return version

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
