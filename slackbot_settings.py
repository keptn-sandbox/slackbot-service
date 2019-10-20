import os
from dotenv import load_dotenv
load_dotenv()

DEBUG = True

API_TOKEN = os.getenv('slackbot_token')

DEFAULT_REPLY = "Sorry but I didn't understand you"

PLUGINS = [
    'keptnbot.plugins'
]
