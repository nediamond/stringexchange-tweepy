from DAL import DAL, Leestner
from credentials import *

import tweepy
import time
import re

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

dal = DAL()
te_handle_re = re.compile(re.escape('@Tweet_Exchanger'), re.IGNORECASE)
def handle_tweet(status):
	if status.text[0:3] != "RT ":
		tweeter = status.user.screen_name
		tweet_id = status.id_str
		tweet_text = te_handle_re.sub('',status.text).strip()
		if not dal.entry_exists(tweet_id):
			return_tweet = dal.get_random_entry()[2]
			return_tweet = "@"+tweeter+' '+return_tweet
			try:
				api.update_status(return_tweet)
				time.sleep(15)
				dal.add_entry(tweeter, tweet_text, tweet_id)
			except Exception as e:
				print e
				print "Tweet failed. Sleeping for 15 minutes..."
				time.sleep(60*15)


listener = Leestner(callback=handle_tweet)
stream = tweepy.Stream(auth=api.auth, listener=listener)
stream.filter(track=['@Tweet_Exchanger'])

		

