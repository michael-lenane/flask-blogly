"""Blogly application."""

from site import USER_SITE
from flask import Flask, render_template, request, redirect, flash
from models import db, connect_db, Users, datetime, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

db.create_all()


@app.route("/")
def home_page():
    """Display home page"""

    users = Users.query.all()
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('start_page.html', users=users, posts=posts)


@app.route('/', methods=["POST"])
def create_user():
    """User submits form that creates a new user"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = Users(first_name=first_name,
                     last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/{new_user.id}")


@app.route('/<int:user_id>')
def show_user(user_id):
    """Show details about selected pet"""
    user = Users.query.get_or_404(user_id)
    posts = Post.query.all()
    return render_template('detail.html', user=user, posts=posts)


@app.route('/edit/<int:user_id>')
def show_edit_page(user_id):

    user = Users.query.get_or_404(user_id)
    return render_template('edit.html', user=user)


@app.route('/edit', methods=["POST"])
def submit_edits():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    user = request.form["current"]

    current_user = Users.query.get_or_404(user)

    current_user.first_name = first_name
    current_user.last_name = last_name
    current_user.image_url = image_url

    db.session.commit()

    return redirect('/')


@app.route('/delete/<int:user_id>')
def delete_user(user_id):

    Users.query.filter(Users.id == user_id).delete()

    db.session.commit()

    return redirect('/')


"""here"""


@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    """Show a form to create a new post for a specific user"""

    user = Users.query.get_or_404(user_id)
    return render_template('add_post.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """Handle form submission for creating a new post for a specific user"""

    user = Users.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    )

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect("/")
