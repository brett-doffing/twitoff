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
    user = DB.relationship("User",  # creates user link between tweets
                           backref=DB.backref("tweets", lazy=True))

    def __repr__(self):
        return "<Tweet: {}>".format(self.text)


def insert_example_users():
    nick = User(id=1, name="Nick")
    elon = User(id=2, name="elonmusk")
    tweet1 = Tweet(id=1, text="Aaaarrrgh, I'm a pirate!", user=nick)
    tweet2 = Tweet(id=2, text="That's it, that's the tweet.", user=nick)
    tweet3 = Tweet(id=3, text="It will come together eventually.", user=nick)
    tweet4 = Tweet(id=4, text="I didn't even inhale.", user=elon)
    tweet5 = Tweet(id=5, text="Space Force is Starlink's army.", user=elon)
    tweet6 = Tweet(id=6, text="I'm flying to Mars tomorrow!!!", user=elon)

    DB.session.add(nick)
    DB.session.add(elon)
    DB.session.add_all([tweet1, tweet2, tweet3, tweet4, tweet5, tweet6])
    DB.session.commit()
