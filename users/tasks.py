from celery import shared_task
import time
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from users.models import CustomUser

@shared_task
def send_otp_email(email, code):
    print("Sending...")
    send_mail(
        "Привет новый пользователь!",
        f"Вот ваш код для подтверждения {code}",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    print("Done")
    return "Ok"

@shared_task
def send_daily_report():
    print("Собираем данные...")
    time.sleep(15)
    print("Успешно")
    return "Ok"
@shared_task
def clear_cache():
    from django.core.cache import cache
    cache.clear()
    print("🧹 Кэш очищен")
    return "Cache cleared"
@shared_task
def save_message_to_file(message):
    with open("messages.txt", "a", encoding="utf-8") as f:
        f.write(message + "\n")
    print(f"💾 Сообщение сохранено: {message}")
    return "Saved"

@shared_task
def send_password_change_reminders():
    

    ninety_days_ago = timezone.now() - timedelta(days=90)
    inactive_users = CustomUser.objects.filter(last_login__lt=ninety_days_ago)

    for user in inactive_users:
        send_mail(
            "Пора сменить пароль",
            "Мы заметили, что вы давно не меняли пароль. "
            "Рекомендуем обновить его для безопасности.",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=True,
        )
    print(f"📧 Напоминания отправлены {inactive_users.count()} пользователям")
    return f"Sent {inactive_users.count()} reminders"