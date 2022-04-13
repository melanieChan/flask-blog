from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

@app.route('/')
def index():
    return render_template('index.html')

# every post has its own link, made using its unique post_id
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

def get_db_connection():
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
