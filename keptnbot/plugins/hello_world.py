# -*- coding: utf-8 -*-
 
from slackbot.bot import respond_to
import re
import json

@respond_to('hello', re.IGNORECASE)
def greet(message):
    attachments = [
    {
        'fallback': 'Fallback text',
        'author_name': 'Hello from Keptn',
        'author_link': 'https://keptn.sh',
        'text': 'An opinionated open-source framework for event-based, automated continuous operations in cloud-native environments.',
        'color': '#59afe1'
    }]
    message.send_webapi('', json.dumps(attachments))