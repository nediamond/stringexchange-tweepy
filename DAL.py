import MySQLdb
import tweepy
from random import choice

class DAL:
    def __init__(self):
        self.db = MySQLdb.connect(
            host='localhost',
            user='root',
            # FIX THIS SHIT
            passwd='cheetos',
            db='tweetexchange',
            )

    def get_random_entry(self):
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM tweets')
        result = cursor.fetchall()
        return choice(result)

    def add_entry(self, user, tweet, tweet_id):
        cursor = self.db.cursor()
        cursor.execute('INSERT INTO tweets (user,tweet,tweet_id) VALUES (%s,%s,%s)', (user,tweet,tweet_id))
        cursor.execute('INSERT INTO tweets_ro (user,tweet,tweet_id) VALUES (%s,%s,%s)', (user,tweet,tweet_id))
        self.db.commit()
        return

    def entry_exists(self, tweet_id):
        cursor = self.db.cursor()
        cursor.execute('SELECT EXISTS(SELECT 1 FROM tweets WHERE tweet_id=%s)',(tweet_id,))
        return bool(cursor.fetchall()[0][0])

    def remove_entry(self, id):
        cursor = self.db.cursor()
        # FIX THIS SHIT
        cursor.execute('DELETE FROM tweets WHERE id='+str(id))
        self.db.commit()
        return

# MOVE THIS TO NEW FILE
class Leestner(tweepy.StreamListener):
    def __init__(self, callback=None):
        tweepy.StreamListener.__init__(self)
        self.callback = callback

    def on_status(self, status):
        self.callback(status)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False
