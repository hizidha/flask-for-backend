from flask import Flask, redirect, url_for, session, render_template, request, flash
import bcrypt
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

app.secret_key = b'20e4d0b360d1ddc6fe6a5ce151feab197f6c39ac703e1830f029ba15dc3f132e'

# Data pengguna yang disimpan dalam bentuk dictionary
user_data = {
    'admin': {
        'password': bcrypt.hashpw(b'adminbesar', bcrypt.gensalt()),
        'login_attempts': 0
    }
}

class InvalidCredentials(HTTPException):
    code = 400
    description = 'Please enter correct username or password.'
    
class TooManyAttempts(HTTPException):
    code = 401
    description = 'Too many login attempts. Please try again later.'


@app.route('/')
def home():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', username=username)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in user_data and bcrypt.checkpw(password.encode('utf-8'), user_data[username]['password']):
            session['username'] = username
            user_data[username]['login_attempts'] = 0
            return redirect(url_for('home'))
        else:
            if username in user_data:
                user_data[username]['login_attempts'] += 1
                if user_data[username]['login_attempts'] >= 3:
                    raise TooManyAttempts
            raise InvalidCredentials
             
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    username = session['username']
    flash(f'See You Again {username}.', 'success')
    session.pop('username', None)
    return redirect(url_for('login'))

@app.errorhandler(InvalidCredentials)
def handle_invalid_credentials(e):
    flash('Please enter correct username or password.', 'error')
    return redirect(url_for('login'))

@app.errorhandler(TooManyAttempts)
def handle_many_attempts(e):
    flash('Too many login attempts. Please try again later.', 'error')
    return redirect(url_for('login'))
