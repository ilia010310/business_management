import smtplib
from email.message import EmailMessage

from celery import Celery
from pydantic import EmailStr

from src.config import settings

celery = Celery("tasks", broker=settings.REDIS_URL)


def get_email_template_dashboard_for_code(email_to: str, code: int):
    email = EmailMessage()
    email["Subject"] = f"{code} - Ваш код подтверждения регистрации на платформе Business Manager"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        "<div>" f'<h1 style="color: black;">Регистрация</h1><br>' f"Код подтверждения: {code}" "</div>", subtype="html"
    )
    return email


def get_email_template_dashboard_for_link(email_to: EmailStr, link: str):
    email = EmailMessage()
    email["Subject"] = f"Ваша ссылка для окончания регистрации на платформе Business Manager"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        "<div>" f'<h1 style="color: black;">Регистрация</h1><br>' f"Перейдите по ссылке и придумайте пароль: {link}" "</div>",
        subtype="html"
    )
    return email


@celery.task
def send_invite_code_to_email(email: str, code: int):
    email = get_email_template_dashboard_for_code(email, code)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(email)


@celery.task
def send_invite_link_to_email(email: EmailStr, link: str):
    email = get_email_template_dashboard_for_link(email, link)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(email)
