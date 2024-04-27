"""Routes for Flask app"""
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app
from flask import render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import select

from my_blog import login_manager
from my_blog.models import db, User, Post
from my_blog.forms import RegistrationForm, LoginForm


@app.route('/')
def index():
    """Index page for Flask app."""
    return render_template('index.html')
