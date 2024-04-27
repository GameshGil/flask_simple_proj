"""Models for main Flask app."""
import datetime as dt

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model, UserMixin):
    """Application user model"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(10), nullable=False)
    hashed_password = db.Column(db.String)
    reg_date = db.Column(db.DateTime, default=dt.datetime.now)
    posts = db.relationship('Post', backref='post_author')

    def __repr__(self):
        return f"<User {self.username}>"


class Post(db.Model):
    """Publications model"""
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)
    author_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<Post {self.id}>"
