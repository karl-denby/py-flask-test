from sys import version
from flask import Flask, redirect, request
from flask_bootstrap import Bootstrap
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<h1>WSGI Works!!!</h1>"

@app.errorhandler(404)
def page_not_found(e):
    return "didn't find that page!"

@app.route('/headers')
def headers():
    user_agent = request.headers.get('User-Agent')
    return 'You are using %s' % user_agent

@app.route('/user/')
@app.route('/user/<name>')
def user(name = ''):
    if len(name) == 0:
        output = '<h1>Hello Stranger</h1>'
    else:
        output =  '<h1>Hello, %s</h1>' % name
    return output

# Run the application
if __name__ == '__main__':
    bootstrap = Bootstrap(app)
    app.run(debug=True, host='0.0.0.0')
