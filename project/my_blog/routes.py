"""Routes for Flask app"""
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app
from flask import render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from my_blog import login_manager
from my_blog.models import db, User
from my_blog.forms import RegistrationForm, LoginForm


@login_manager.user_loader
def load_user(user_id):
    user = db.session.get(User, user_id)
    return user


@app.route('/')
def index():
    """Index page for Flask app."""
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page."""
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        role = form.role.data
        password = form.password.data
        password_repeat = form.password_repeat.data
        if password != password_repeat:
            return render_template(
                'register.html',
                form=form,
                message='Ошибка при вводе пароля'
            )
        if User.query.filter(User.email == email).first():
            return render_template(
                'register.html',
                form=form,
                message='Пользователь уже зарегистрирован'
            )
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            role=role,
            hashed_password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember_me.data
        user = User.query.filter_by(email=email).first_or_404()

        if user and check_password_hash(user.hashed_password, password):
            login_user(user, remember=remember)
            return redirect(url_for('index'))
        return render_template('login.html', form=form)

    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    """User logout page."""
    logout_user()
    return redirect(url_for('login'))


@app.route('/me')
@login_required
def get_user_info():
    """User info page."""
    return f'Информация о пользователе {current_user}.'


@app.errorhandler(401)
def not_authorized(error):
    return render_template('401.html', error=error), 401


@app.errorhandler(403)
def not_permitted(error):
    return render_template('403.html', error=error), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error), 404
