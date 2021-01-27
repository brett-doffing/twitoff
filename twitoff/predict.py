"""Prediction of Users based on Tweet embeddings"""
from .models import User
from .twitter import update_or_add_user, vectorize_tweet
from sklearn.linear_model import LogisticRegression
import numpy as np


def predict_user(user_0_name, user_1_name, tweet_example):
    """
    Determine who is more likely to say a hypothetical tweet.

    Example run: predict_user("elonmusk", "jackblack", "Gamestonks!!")
    Returns 0 or 1 according to predicted user
    """

    user_0 = User.query.filter(User.name == user_0_name).one()
    user_0_vects = np.array([tweet.vect for tweet in user_0.tweets])

    user_1 = User.query.filter(User.name == user_1_name).one()
    user_1_vects = np.array([tweet.vect for tweet in user_1.tweets])

    num_tweets_0 = len(user_0.tweets)
    num_tweets_1 = len(user_1.tweets)

    # Set the number of tweets for each user equal to
    # the minimum number of tweets a user has between the two
    # in order to offset the bias related to unequally sized data
    num_tweets = num_tweets_0 if num_tweets_0 <= num_tweets_1 else num_tweets_1

    # Vertically stack embedding arrays of equal size
    vects = np.vstack([user_0_vects[:num_tweets], user_1_vects[:num_tweets]])

    # collection of labels equal to the length of vects
    labels = np.concatenate(
        [np.zeros(num_tweets), np.ones(num_tweets)])

    # train logistic regression
    log_reg = LogisticRegression().fit(vects, labels)

    # vectorizing tweet_example
    example_tweet_vec = vectorize_tweet(tweet_example)

    # runs prediction and return 0 or 1
    return log_reg.predict(np.array(example_tweet_vec).reshape(1, -1))
