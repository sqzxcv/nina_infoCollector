from apscheduler.schedulers.blocking import BlockingScheduler

def job():
    # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    pass
# BlockingScheduler
scheduler = BlockingScheduler()
scheduler.add_job(job, 'cron', day_of_week='1-5', hour=6, minute=30)
scheduler.start()