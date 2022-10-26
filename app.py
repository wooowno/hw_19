from flask import Flask
from flask_restx import Api

from config import Config
from dao.model.user import User
from setup_db import db
from views.auth import auth_ns
from views.directors import director_ns
from views.genres import genre_ns
from views.movies import movie_ns
from views.user import user_ns


def create_app(config_object):
    application = Flask(__name__)

    application.config.from_object(config_object)
    application.app_context().push()

    register_extensions(application)

    return application


def register_extensions(application):
    db.init_app(application)
    api = Api(application)

    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)


def create_data():
    db.create_all()

    u1 = User(username="vasya", password="my_little_pony", role="user")
    u2 = User(username="oleg", password="qwerty", role="user")
    u3 = User(username="olga", password="P@ssw0rd", role="admin")

    with db.session.begin():
        db.session.add_all([u1, u2, u3])


app = create_app(Config())
app.debug = True

if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)
