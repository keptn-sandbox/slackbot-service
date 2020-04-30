# -*- coding: utf-8 -*-

from slackbot.bot import respond_to
import re
import json

@respond_to(r'deployment-finished (.*)', re.IGNORECASE)
def deployment_finished(message, args):
    reply = []
    reply.append(u'•`{0}`'.format('@<Botname> ' + args))
    message.send(u'\n'.join(reply))
