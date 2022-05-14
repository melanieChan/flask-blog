from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import abort
import os
from flask_utils import get_db_path
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

# pipenv shell
# export FLASK_APP=app
# export FLASK_ENV=development
# flask run

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

local_path = os.path.abspath(os.path.dirname(__file__))

# database
# adds db file to project directory
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + get_db_path()
db = SQLAlchemy(app)

# create db:
# pipenv shell
# flask shell
# from app import db, Post
# db.create_all()
# db.drop_all()
# parietal = Post(title='parietal lobe', content='sensory')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    title = db.Column(db.Text)
    content = db.Column(db.Text)

    def __repr__(self):
        return f'Post about {self.title}: {self.content} ({self.created})'

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

# every post has its own link, made using its unique post_id
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

# find a post from db given its post_id
def get_post(post_id):
    post = Post.query.filter_by(id=post_id).first()

    if post is None:
        abort(404)
    return post

# gets user's inputs for a new post and saves it as an entry in the posts table
@app.route('/', methods=('GET', 'POST'))
def write_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        # any error will causes page to refresh and flash message will appear after refresh
        if len(title) < 1:
            flash('Please enter a valid title')
        else:
            # get input and store it as a new post
            new_post = Post(title=title, content=content)
            db.session.add(new_post)
            db.session.commit()

            # go back to home page to see new post appended to list
            return redirect(url_for('index'))

    return render_template('index.html')

# delete a post
@app.post('/<int:post_id>/delete/')
def delete(post_id):
    post_to_delete = Post.query.get_or_404(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()

    # go back to home page
    return redirect(url_for('index'))
