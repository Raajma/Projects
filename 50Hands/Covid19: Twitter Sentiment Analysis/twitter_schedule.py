import tweet_server
import schedule
import os

def timed_job():
	tweet_server.tweetSentiment()

        
	#tweet_server.printer()


schedule.every().day.at("01:00").do(timed_job)
#tweet_server.printer();

while True:
    schedule.run_pending()
