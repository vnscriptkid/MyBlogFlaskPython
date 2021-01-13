from flask import render_template, flash, redirect, session, url_for

from app import app, db
from app.forms import LoginForm
from app.models import User
from app.mail import send_email


@app.route('/')
@app.route('/index')
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

    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            user = User(username=form.username.data)
            db.session.add(user)
            db.session.commit()
            send_email('thanhnt2195@gmail.com', 'New User', # send mail to admin to notify about new user
                       'mail/new_user', user=user)
            session['known'] = False
        else:
            session['known'] = True
            form.username.data = ''
        session['username'] = form.username.data
        return redirect(url_for('login'))
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           username=session.get('username'),
                           known=session.get('known'))


