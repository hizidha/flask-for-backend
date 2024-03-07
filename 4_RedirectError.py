from flask import Flask, redirect, url_for, abort
from werkzeug.exceptions import HTTPException

app = Flask(__name__)


# default redirect
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return 'halaman login'


# redirect with param
@app.get('/redirect_to_profile')
def redirect_profile():
    return redirect(url_for('show_user_profile', username='John Doe'))

@app.get('/user/profile/<username>')
def show_user_profile(username):
    return f'{username}\'s profile.'


# error handling
@app.route('/profile/')
def profiles():
    abort(401)
    this_is_never_executed()
    
def this_is_never_executed():
    print("This function is never executed.")
    
# custom handler for error
# @app.errorhandler(401)
# def page_not_found(error):
#     return "Unauthenticated, Please Login", 401

# custom exception & handler
class InvalidCredentials(HTTPException):
    code = 401
    description = 'Please enter correct username or password.'

# config errorhandler and redirect | jika belum login mengarahkan ke halaman login 
@app.errorhandler(InvalidCredentials)
def handler_invalid_credential(e: InvalidCredentials):
    return redirect('/login')

@app.route('/handlers')
def index2():
    raise InvalidCredentials