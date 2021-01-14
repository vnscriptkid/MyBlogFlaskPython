from threading import Thread
from flask import render_template
from flask_mail import Message
from app import mail


def send_async_email(current_app, msg):
    with current_app.app_context():
        mail.send(msg)


def send_email(app, to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return thread

