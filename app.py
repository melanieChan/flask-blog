from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import abort
import os
from flask_utils import download_database

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

@app.route('/')
def index():
    posts = get_posts()
    return render_template('index.html', posts=posts)

# every post has its own link, made using its unique post_id
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

def get_db_connection():
    dir_path = os.path.abspath(os.path.dirname(__file__)) # path of current file's directory

    # check if there's a file named database.db
    db_file_exists = os.path.isfile(os.path.join(dir_path, 'database.db'))

    if not db_file_exists: # download the database if it doesn't already exist
        download_database()

    # connect to db
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

# find a post from db given its post_id
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',(post_id,)).fetchone()
    connection.close()

    # show 'Not Found' page if post doesn't exist
    if post is None:
        abort(404)
    return post

# retrieve all posts from db
def get_posts():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    print(posts)

    if posts is None:
        return []
    return posts

# gets user's inputs for a new post and saves it as an entry in the posts table
@app.route('/', methods=('GET', 'POST'))
def write_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if len(title) < 1:
            flash('Please enter a valid title')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',(title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('index.html')
