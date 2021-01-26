""""Main app/routing file for Twitoff."""

from os import getenv
from flask import Flask, render_template
from .models import DB, User, insert_example_users
from .twitter import update_or_add_user


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv('DATABASE_URI')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)

    @app.route('/')
    def root():
        # Drop for the sake of dropping
        # DB.drop_all()

        # `checkfirst` argument defaults to True, and will therefore
        # not create a table if it already exists.
        # DB.create_all()

        return render_template('base.html', title='Home',
                               users=User.query.all())

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Home')

    @app.route('/update')
    def update():
        update_or_add_user("elonmusk")
        return render_template('base.html', title="Home",
                               users=User.query.all())

    return app
