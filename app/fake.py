from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, Post


def _insert_user(email, username, password, confirmed=True, name="", location="", about_me=""):
    u = User(email=email,
             username=username,
             password=password,
             confirmed=confirmed,
             name=name,
             location=location,
             about_me=about_me)
    db.session.add(u)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


def users(count=100):
    _insert_user(email="thanh@gmail.com", username="thanh", password="123456", confirmed=True)
    fake = Faker()
    i = 0
    while i < count:
        _insert_user(
            email=fake.email(),
            username=fake.user_name(),
            password="123456",
            name=fake.name(),
            confirmed=True,
            location=fake.city(),
            about_me=fake.text(),
        )
        i += 1


def posts(count=100):
    fake = Faker()
    user_count = User.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        p = Post(body=fake.text(),
            timestamp=fake.past_date(),
            author=u)
        db.session.add(p)
        db.session.commit()

