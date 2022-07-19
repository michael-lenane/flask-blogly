"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Users (db.Model):
    __table_name__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(20),
                           nullable=False,)

    last_name = db.Column(db.String(20),
                          nullable=False)

    image_url = db.Column(db.String,
                          nullable=True,
                          default="https://www.istockphoto.com/photos/profile-avatar")
