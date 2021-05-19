from crontab import CronTab


cron = CronTab(user='dell')
job = cron.new(command='python3 example.py')
job.minute.every(1)
print(job.is_enabled())
cron.write()