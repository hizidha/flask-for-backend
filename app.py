import os, uuid, mimetypes
from werkzeug.utils import secure_filename

from flask import Flask, url_for, request, make_response, render_template, jsonify
from users import valid_login, log_the_user_in

app = Flask(__name__)


# @app.route('/')
# def index():
#     return "Index Page"

@app.get('/')
def form():
    html = """
        <form action="/" method="POST">
            <label for="first_name">Name File</label>
            <input type="text" id="first_name" name="first_name">
            <input type="submit">
        </form>
    """
    return html

@app.post('/')
def post_form():
    first_name = request.form.get("first_name")
    return f'Your first name is {first_name}'


@app.get('/lag/')
def upload_form():
    html2 = """
        <form action="/lag/" enctype="multipart/form-data" method="POST">
            <label for="name_file">Name File</label>
            <input type="text" id="name_file" name="name_file">
            <input type="file" id="file_input" name="file_input">
            <input type="submit">
        </form>
    """
    return html2

@app.post('/lag/')
def post_upload_form():
    name_of_file = request.form.get("name_file")
    files_up = request.files.get("file_input")
    
    # Get file extension
    filename_with_ext = secure_filename(files_up.filename)
    ext = filename_with_ext.rsplit('.', 1)[-1]  # Get the extension
    
    # Generate a unique identifier
    unique_identifier = str(uuid.uuid4())[:10]  # Get the first 10 characters of a UUID
    
    # Secure the filename and combine it with the unique identifier and the file extension
    filename = secure_filename(name_of_file) + '_' + unique_identifier + '.' + ext
    
    # Save the file
    files_up.save(os.path.join("./cache/file_uploaded_users", filename))
    
    return f'File dengan nama {name_of_file}, berhasil disimpan dengan nama unik: {filename}'


@app.route('/header/')
def show_header():
    return request.headers.get('User-Agent')

@app.route('/elearning')
def show_list_elearning():
    author = request.args.get('author', 'default-value') # bisa kosong untuk default-value
    return author

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid Username or Password.'
            
    return render_template('login.html', error=error)       
    #return "Login Page"

# @app.route('/hello/')
# def hello_world():
#     return "Hello World MySkill!"

@app.route('/profile/user/<username>/')
def profile(username):
    return f"{username}\'s profile"

@app.route('/post/<int:post_id>/')
def view_post(post_id):
    return f'Post with post_id:{post_id}'

@app.route('/path/<path:subpath>/')
def view_path(subpath):
    return f'Subpath: {subpath}'

@app.route('/url')
def url():
    return f'''
            <p>{url_for('index')}</p>
            <p>{url_for('login')}</p>
            <p>{url_for('login', next='/')}</p> 
            <p>{url_for('profile', username='JonhDoe')}</p>
            '''
            
            
@app.route('/response/')
def hay():
    response = make_response('hello')
    response.status_code = 200
    return response

@app.route('/dict/') # implementation for jsonify
def dict_jsonify():
    data = {
        'name': 'adisaputra zidha',
        'age': 20,
        'city': 'surabaya'
    }
    # response = jsonify(data) sudah tidak perlu digunakan kembali
    return data
