"""
APScheduler

Docs: http://apscheduler.readthedocs.io/en/latest/userguide.html
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class Scheduler:

    scheduler = None

    COLLECTION_JOBS = 'app_jobs'

    functions = {}

    def __init__(self, core):
        self.core = core
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()
        self.table = self.core.db[self.COLLECTION_JOBS]

    def setFunctions(self, functions={}):
        """
        Dictionary "label" -> "function"

        :param functions dict:
            'print': print
            'checkFeeds': test.getFeed
        """
        for label in functions:
            self.functions[label] = functions[label]

    def runJob(self, params):
        label = params['label']
        job_function = self.functions[label]
        trigger = params['trigger']
        func_args = params['func_args']
        trigger_params = params['trigger_params']
        job_id = params['job_id']

        return self.scheduler.add_job(job_function, trigger, **trigger_params, args=func_args, id=job_id)


    def addJob(self, label, func_args=[], trigger='', trigger_params=[], job_id=''):
        """
        core.scheduler.addJob(
            label='message',
            func_args=['blet'],
            trigger='cron',
            trigger_params={'minute': '*'},
            job_id=getJobId('message', chat_id)
        )
        """
        try:
            job_params = {
                'label': label,
                'func_args': func_args,
                'trigger': trigger,
                'trigger_params': trigger_params,
                'job_id': job_id
            }


            if self.scheduler.get_job(job_id):
                self.removeJob(job_id)

            # run job
            self.runJob(job_params)

            # save job to db
            self.table.insert_one(job_params)
        except Exception as e:
            self.core.logger.error(e, exc_info=e)

    def removeJob(self, job_id):
        """
        core.scheduler.removeJob(getJobId('message', chat_id))
        """
        try:
            if self.scheduler.get_job(job_id):
                self.scheduler.remove_job(job_id)
                self.table.remove({'job_id': job_id})
        except Exception as e:
            self.core.logger.error(e, exc_info=e)

    def restoreJobs(self):
        try:
            # get jobs from db
            jobs = self.table.find()

            # run jobs
            for job in jobs:
                self.runJob(job)
        except Exception as e:
            self.core.logger.error(e, exc_info=e)

"""
core.scheduler.add_job(taly.BOT.sendMessage, 'interval', seconds=5, args=['text'])

## Add job

http://apscheduler.readthedocs.io/en/latest/modules/triggers/interval.html
> scheduler.add_job(tick, 'interval', seconds=1)
weeks (int) – number of weeks to wait
days (int) – number of days to wait
hours (int) – number of hours to wait
minutes (int) – number of minutes to wait
seconds (int) – number of seconds to wait

http://apscheduler.readthedocs.io/en/latest/modules/triggers/cron.html
> scheduler.add_job(tick, trigger='cron', minute='*/5')
year (int|str) – 4-digit year
month (int|str) – month (1-12)
day (int|str) – day of the (1-31)
week (int|str) – ISO week (1-53)
day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
hour (int|str) – hour (0-23)
minute (int|str) – minute (0-59)
second (int|str) – second (0-59)

http://apscheduler.readthedocs.io/en/latest/modules/triggers/date.html
> sched.add_job(my_job, 'date', run_date='2009-11-06 16:30:05', args=['text'])
> sched.add_job(my_job, 'date', run_date=datetime(2009, 11, 6, 16, 30, 5), args=['text'])
tick — function to run

date: use when you want to run the job just once at a certain point of time
interval: use when you want to run the job at fixed intervals of time
cron: use when you want to run the job periodically at certain time(s) of day
"""
