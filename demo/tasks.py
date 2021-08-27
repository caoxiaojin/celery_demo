from celery import shared_task
import time

@shared_task()
def add(x,y):
    time.sleep(120)
    return x + y

@shared_task()
def mul(x,y):
    time.sleep(120)
    return x * y

@shared_task()
def crontest():
    with open('/opt/cron.log', mode='a', encoding='utf-8') as f:
        data = str(time.time())
        f.write(data)
        f.write('\n')

@shared_task()
def crontestargs(x):
    with open('/opt/cron1.log', mode='a', encoding='utf-8') as f:
        data = str(time.time()) + "  args:" + str(x)
        f.write(data)
        f.write('\n')