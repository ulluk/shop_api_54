

from celery import shared_task
import time

@shared_task
def send_otm_email():
    print("Sending..")
    return "OK"

@shared_task
def send_daily_report():
    print("Собираем данные")
    time.sleep(15)
    print("Успешно")
    return "OK"