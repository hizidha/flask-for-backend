from flask import Flask, session, redirect, url_for

app = Flask(__name__)

# Set the secret key to some random bytes.
# Make a secret key
# import secrets
# print(secrets.token_hex())
app.secret_key = b'20e4d0b360d1ddc6fe6a5ce151feab197f6c39ac703e1830f029ba15dc3f132e'


@app.get('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'

@app.get('/login/<username>')
def login(username):
    session['username'] = username
    return redirect(url_for('index'))

@app.get('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


# Flash: variabel session yang bisa diakses 1 kali saja
from flask import flash, get_flashed_messages

@app.get('/home')
def home():
    flash('home')
    return redirect('/target')

@app.get('/target')
def target():
    messages = get_flashed_messages()
    if len(messages) > 0:
        return f'You came from {messages[0]}'
    return 'Where did you come from?'

@app.get('/categories')
def cat():
    flash('1', 'success')
    flash('2', 'error')
    flash('3', 'info')
    messages = get_flashed_messages(with_categories=True)
    return messages
    