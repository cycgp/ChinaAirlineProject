from apscheduler.schedulers.blocking import BlockingScheduler

def some_job():
    print('Decorated job')

scheduler = BlockingScheduler()
scheduler.add_job(some_job, 'interval', seconds=2)
scheduler.start()
