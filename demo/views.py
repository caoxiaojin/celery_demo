from rest_framework.views import APIView
from utils.core import MyResponse
from django.http import JsonResponse
from celery.result import AsyncResult
from celery_demo import celery_app
from demo import tasks
from django_celery_results.models import TaskResult
from django_celery_beat.models import PeriodicTask
from django_celery_beat.models import IntervalSchedule
import json
from django_celery_beat.models import CrontabSchedule
import pytz
# Create your views here.

class TaskView(APIView):
    def get(self,request):
        response = MyResponse()
        nid = request.GET.get("nid", None)
        if nid:
            result_object = AsyncResult(id=nid, app=celery_app)
            response.data = result_object.status
        return JsonResponse(response.get_dic)

    def post(self, request):
        response = MyResponse()
        x = request.data['x']
        y = request.data['y']
        result = tasks.add.delay(int(x),int(y))
        task_result = TaskResult(task_id=result.id)
        task_result.save()
        response.data = result.id
        return JsonResponse(response.get_dic)

class CronEveryView(APIView):
    def get(self,request):
        response = MyResponse()
        every = request.GET.get("every", 10)
        schedule, created = IntervalSchedule.objects.get_or_create(every=int(every), period=IntervalSchedule.SECONDS)
        print(schedule,created)
        PeriodicTask.objects.create(interval=schedule, name='demo.tasks.crontest', task='demo.tasks.crontest')
        return JsonResponse(response.get_dic)

    def post(self,request):
        response = MyResponse()
        every = request.data['every']
        x = request.data['x']
        schedule, created = IntervalSchedule.objects.get_or_create(every=int(every), period=IntervalSchedule.SECONDS)
        print(schedule, created)
        PeriodicTask.objects.create(interval=schedule, name='demo.tasks.crontestargs', task='demo.tasks.crontestargs',
                                    args=json.dumps([x]))
        return JsonResponse(response.get_dic)

class CronView(APIView):
    def get(self,request):
        response = MyResponse()
        schedule, _ = CrontabSchedule.objects.get_or_create(
        minute = '*/1',
        hour = '*',
        day_of_week = '*',
        day_of_month = '*',
        month_of_year = '*',
        timezone = pytz.timezone('Asia/Shanghai'))
        PeriodicTask.objects.create(
        crontab = schedule,
        name = 'demo.tasks.crontest',
        task = 'demo.tasks.crontest',)
        return JsonResponse(response.get_dic)
