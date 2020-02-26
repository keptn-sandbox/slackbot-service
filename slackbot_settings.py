import os
from dotenv import load_dotenv

# loading environment variables
load_dotenv()

DEBUG = False

API_TOKEN = os.getenv('slackbot_token')

DEFAULT_REPLY = "Sorry, but I didn't understand you"

PLUGINS = [
    'keptnbot.plugins'
]

EVALUATION_TIMEOUT=300
TRUST_SELFSIGNED_SSL=False