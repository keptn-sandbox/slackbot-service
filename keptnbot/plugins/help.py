from slackbot.bot import respond_to
import re
import json

@respond_to('help$', re.IGNORECASE)
def hello_reply(message):
    reply = []
    reply.append(u'•`{0}`'.format('@KeptnBot start-evaluation <project> <service> <stage> <start> <end> | Send start-evaluation event. <start> & <end> date time should be in ISO format (2019-12-13T13:00)'))
     
    message.send(u'\n'.join(reply))
