import asyncio

from celery import shared_task

from bot.main_bot import send_newsletter_bot
from wanmark.models import NewsletterBot


@shared_task()
def send_bot(nl_id):
    print(1111)
    nl: NewsletterBot = NewsletterBot.objects.get(id=nl_id)
    nl.status = 1
    nl.save()
    asyncio.run(send_newsletter_bot(nl_id))
