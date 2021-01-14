from flask import render_template, redirect, session, url_for
from datetime import datetime

from app.main import main


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

