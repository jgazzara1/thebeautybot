# Python Final Project 12/16/20
# Beauty Bot

# Importing necessary modules 
import tweepy
import logging
import time
import random

# This is the list of compliments or insults
look = ["beautiful", "ugly", "sexy", "stupid", "happy", "delecate", "dazzling", "foxy", "dirty", "busy"]

# Authenticate to Twitter
auth = tweepy.OAuthHandler("classified", "classified")
auth.set_access_token("classified", "classified")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Checking my account mentions
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

            # This follows the user
            if not tweet.user.following:
                tweet.user.follow()

            # This generates the tweet
            api.update_status(status = 'You look ' + random.choice(look) + ' today!', in_reply_to_status_id = tweet.id , auto_populate_reply_metadata=True)
            
    return new_since_id


def main():
    api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)
    since_id = 1
    while True:
        since_id = check_mentions(api, ["how", "look"], since_id) # Searching for phrases 'how' and 'look'
        logger.info("Waiting...")
        time.sleep(30)                                            # Runs every 30 seconds 

if __name__ == "__main__":
    main()
