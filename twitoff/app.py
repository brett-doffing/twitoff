""""Main app/routing file for Twitoff."""

from os import getenv
from flask import Flask, render_template, request
from .models import DB, User
from .twitter import update_or_add_user
from .predict import predict_user


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv('DATABASE_URI')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)

    @app.route('/')
    def root():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Home',
                               users=User.query.all())

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Home')

    @app.route('/update', methods=["POST"])
    def update():
        update_or_add_user(request.values["user_name"])
        return render_template('base.html', title="Home",
                               users=User.query.all())

    @app.route('/compare', methods=["POST"])
    def compare():
        user_0, user_1 = sorted(
            [request.values["user1"], request.values["user2"]])

        if user_0 == user_1:
            message = "Cannot compare users to themselves?!"
        else:
            prediction = predict_user(
                user_0,
                user_1,
                request.values["tweet_text"]
            )
            message = "{} is more likely to be said by {} than {}".format(
                                        request.values["tweet_text"],
                                        user_1 if prediction else user_0,
                                        user_0 if prediction else user_1
                                    )

        return render_template('prediction.html', title="Prediction",
                               message=message)

    @app.route("/user", methods=["POST"])
    @app.route("/user/<name>", methods=["GET"])
    def user(name=None, message=""):
        name = name or request.values["user_name"]
        try:
            if request.method == "POST":
                update_or_add_user(name)
                message = "User {} was successfully added.".format(name)

            tweets = User.query.filter(User.name == name).one().tweets

        except Exception as e:
            message = "Error adding {}: {}".format(name, e)
            tweets = []

        return render_template("user.html", title=name,
                               tweets=tweets, message=message)

    return app


if __name__ == '__main__':
    create_app()
