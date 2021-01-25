"""SQLAlchemy models and utility functions for TwitOff"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class User(DB.Model):  # User Table
    """Twitter Users corresponding to Tweets"""
    id = DB.Column(DB.BigInteger, primary_key=True)  # id column
    name = DB.Column(DB.String, nullable=False)  # name column

    def __repr__(self):
        return "<User: {}>".format(self.name)


class Tweet(DB.Model):
    """Tweets corresponding to Users"""
    id = DB.Column(DB.BigInteger, primary_key=True)  # id column
    text = DB.Column(DB.Unicode(300))  # tweet text column - allows for emojis
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        "user.id"), nullable=False)  # user_id column (corresponding user)
    user = DB.relationship("User",
                           backref=DB.backref("tweets", lazy=True))  # creates user link between tweets

    def __repr__(self):
        return "<Tweet: {}>".format(self.text)


# def insert_example_users():
#     nick = User(id=1, name="Nick")
#     elon = User(id=2, name="elonmusk")
#     DB.session.add(nick)
#     DB.session.add(elon)
#     DB.session.commit()