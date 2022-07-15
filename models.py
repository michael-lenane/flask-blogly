"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy


class Users (db.Model):
    __table_name__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(20),
                           nullable=False,)

    last_name = db.Column(db.String(20),
                          nullable=False)

    image_url = db.Column(db.URL,
                          nullable=True,
                          default="https://www.istockphoto.com/photos/profile-avatar")
