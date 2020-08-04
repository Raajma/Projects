import chatbot_test
import schedule
import os

def timed_job():
	if os.path.exists("news.csv"):
		os.remove("news.csv")
	if os.path.exists("general.csv"):
		os.remove("general.csv")
	chatbot_test.extract()

schedule.every().day.at("08:01").do(timed_job)
schedule.every().day.at("20:10").do(timed_job)
#chatbot_test.printer();

while True:
    schedule.run_pending()
