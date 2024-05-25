import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import telebot
from aiosmtplib import SMTP
import asyncio

logger = telebot.logger


async def send_mail(subject, msg, hostname, port, username, password, use_tls, email_to):
    message = MIMEMultipart()
    message["From"] = username
    message["To"] = email_to
    message["Subject"] = subject
    message.attach(MIMEText(f"<html><body>{msg}</body></html>", "html", "utf-8"))

    smtp_client = SMTP(hostname=hostname, port=port, use_tls=use_tls)
    async with smtp_client:
        await smtp_client.login(username, password)
        errors, response = await smtp_client.send_message(message)
        logger.info(f'Отправлена почта:\nСтатус: {errors}, {response}\n{msg}')

if __name__ == '__main__':
    asyncio.run(send_mail('Тема письма', 'gau@23132132.ru', '<h1>Привет</h1>'))
