#!/usr/bin/env python

import sys
import logging
import logging.config
from slackbot.bot import Bot
import slackbot_settings

from flask import Flask
import threading

from webapp import routes

def main():
    kw = {
        'format': '[%(asctime)s] %(message)s',
        'datefmt': '%m/%d/%Y %H:%M:%S',
        'level': logging.DEBUG if slackbot_settings.DEBUG else logging.INFO,
        'stream': sys.stdout,
    }
    logging.basicConfig(**kw)
    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)

    try:
        bot = Bot()
        bot.run()
    except Exception as e:
        print(e)

app = Flask(__name__)

app.register_blueprint(routes.keptn_webserver)

if __name__ == "__main__":
    t = threading.Thread(target=main)
    t.daemon = True
    t.start()
    app.run(debug=True)