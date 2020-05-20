# -*- coding: utf-8 -*-

from slackbot.bot import respond_to
import re
import json

@respond_to('help$', re.IGNORECASE)
def help_reply(message):
    reply = []
    reply.append(u'•`{0}`'.format('@<Botname> start-evaluation <project> <service> <stage> <minutes> | example: @Botname start-evaluation <project> <service> <stage> 10'))
    reply.append(u'•`{0}`'.format('@<Botname> start-evaluation <project> <service> <stage> <start-time> <end-time> | example: @Botname start-evaluation <project> <service> <stage> 12:00 12:15'))
    reply.append(u'•`{0}`'.format('@<Botname> start-evaluation <project> <service> <stage> <date> <start-time> <end-time> | example: @Botname start-evaluation <project> <service> <stage> 30/01/2020 12:00 12:15'))

    reply.append(u'•`{0}`'.format('@<Botname> deployment-finished <project> <service> <stage> <test-strategy> <deployment-url> | example: @Botname deployment-finished myproject myservice myproduction myteststrategy https://myservice.myproject.com/'))
    message.send(u'\n'.join(reply))
