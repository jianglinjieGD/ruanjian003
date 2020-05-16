from apscheduler.schedulers.blocking import BlockingScheduler
import datetime


def aps_test():
    print(datetime.datetime.now())


scheduler = BlockingScheduler()
scheduler.add_job(func=aps_test, trigger="cron", second="*/5")
scheduler.start()



