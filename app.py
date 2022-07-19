"""Blogly application."""

from site import USER_SITE
from flask import Flask, render_template, request, redirect
from models import db, connect_db, Users
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
    return render_template('start_page.html', users=users)


@app.route('/<int:user_id>')
def show_pet(user_id):
    """Show details about selected pet"""
    user = Users.query.get_or_404(user_id)
    return render_template('detail.html', user=user)


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
