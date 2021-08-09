from celery import Celery
from django.core.mail import send_mail

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
def send_mail_to(subject, message, receivers):
    send_mail(subject, message, 'admin@admin', [receivers])