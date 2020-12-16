#Python Final Project 12/16/20
#Beauty Bot

import tweepy
import logging
import time
import random

look = ["beautiful", "ugly", "sexy", "stupid", "happy", "delecate", "dazzling", "foxy", "dirty", "busy"]

# Authenticate to Twitter
auth = tweepy.OAuthHandler("2TFr9GhiwSrnsxXktoZkWJtt1", "qFjTrsY0gubhtKvar2AWpGJEhIzAYOD943cZcJu5pOJ6InQwhZ")
auth.set_access_token("1339325491111669761-o4e7fW0mS9XpGTFOeeEcI1d42MteQE", "XMVo0mjw3I7NHNC78euCs1gPwTwPqUu6RqzBVh51VhEbK")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            print("Answering to ", tweet.user.name)

            if not tweet.user.following:
                tweet.user.follow()

            api.update_status(status = 'You look ' + random.choice(look) + ' today!', in_reply_to_status_id = tweet.id , auto_populate_reply_metadata=True)
            
    return new_since_id

def main():
    api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)
    since_id = 1
    while True:
        since_id = check_mentions(api, ["how", "look"], since_id)
        logger.info("Waiting...")
        time.sleep(30)

if __name__ == "__main__":
    main()
