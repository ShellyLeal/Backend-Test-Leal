from __future__ import absolute_import, unicode_literals
from django.conf import settings
from celery import shared_task
from slack import WebClient
from .utils import spawn_uuid


@shared_task
def slack_advertisement(uuid_key):
    '''A function that notifies
    the today's lunch in a Slack
    channel

    :param uuid_key: the today's uuid_key
    '''
    token = settings.OAUTH_ACCESS_TOKEN
    client = WebClient(token=token)
    entry = 'Hi! Peek an eye to today\'s menu at:'
    notice = entry + settings.URL + str(uuid_key)
    client.api_call(
        'chat.postMessage', 
        json={
            'channel': settings.CHANNEL,
            'text': notice,
        },
    )
