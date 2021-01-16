from flask import render_template, redirect, session, url_for
from datetime import datetime

from flask_login import login_required

from app.decorators import admin_required, permission_required
from app.main import main
from app.models import Permission


@main.route('/')
@main.route('/index')
def index():
    user = {'username': 'thanh'}

    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    return render_template(
        'index.html',
        title='Home',
        user=user,
        posts=posts,
        current_time=datetime.utcnow()
    )


@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "For comment moderators!"

