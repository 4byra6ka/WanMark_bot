import asyncio

from celery import shared_task

from bot.main_bot import send_newsletter_bot
from wanmark.models import NewsletterBot


@shared_task
def send_bot(nl_id):
    """Отправка рассылки новостей"""
    nl: NewsletterBot = NewsletterBot.objects.get(id=nl_id)
    asyncio.run(send_newsletter_bot(nl))
