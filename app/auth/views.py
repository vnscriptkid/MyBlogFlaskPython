from app.auth import auth
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from ..models import User
from .forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next_path = request.args.get('next')
            if next_path is None or not next_path.startswith('/'):
                next_path = url_for('main.index')
            return redirect(next_path)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    pass


@auth.route('/register', methods=['GET', 'POST'])
def register():
    pass

