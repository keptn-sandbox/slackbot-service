# -*- coding: utf-8 -*-

from slackbot.bot import respond_to
import re
import json
import os
import time
import datetime
import logging
import requests
import slackbot_settings
from keptnbot.plugins import utils

keptn_host = os.getenv('keptn_host')
keptn_token = os.getenv('keptn_api_token')
bridge_url = os.getenv('bridge_url')
headers = {'x-token': keptn_token, 'Content-Type': 'application/json'}

def send_event(project, service, stage, test_strategy, deployment_uri):
    body = {
      "type": "sh.keptn.events.deployment-finished",
      "specversion": "0.2",
      "source": "https://github.com/keptn-sandbox/slackbot-service",
      "contenttype": "application/json",
      "data": {
        "project": project,
        "stage": stage,
        "service": service,
        "testStrategy": test_strategy,
        "labels": {
          "runby": "KeptnBot"
        },
        "deploymentURIPublic": deployment_uri
      }
    }

    logging.info(body)

    res = requests.post(url=keptn_host+"/api/v1/event", headers=headers, data=json.dumps(body), verify=slackbot_settings.TRUST_SELFSIGNED_SSL)
    res_json = res.json()
    logging.info(res_json)
    keptn_context = res_json['keptnContext']
    token = res_json['token']
    
    return keptn_context

# deployment-finished project service stage test_strategy deploymentURI
@respond_to(r'deployment-finished (.*)', re.IGNORECASE)
def deployment_finished(message, args):
    try:
        args_list = args.split(' ')
        
        # removing empty strings from args list
        args_list = list(filter(None, args_list))
        logging.info(args_list)
        project, service, stage, test_strategy, deployment_uri = '','','','',''

        if(len(args_list) != 5):
            message.reply("`Incorrect number of arguments!`")
            logging.error("Incorrect number of arguments!")
            return
        
        project = args_list[0]
        service = args_list[1]
        stage   = args_list[2]
        test_strategy = args_list[3]
        deployment_uri = args_list[4].replace('>','').replace('<', '')

        if(test_strategy == "none"):
          test_strategy=""

        keptn_context = send_event(project, service, stage, test_strategy, deployment_uri)
        logging.info(keptn_context)

        bridgelink=""
        if (str(bridge_url) != ""):
          bridgelink = "\nFollow <"+ str(bridge_url) + "trace/" + str(keptn_context)+"|along in the bridge> if you want." 
        message.send('Tests & evaluation triggered! ' + str(bridgelink))

        try:
          utils.get_evaluation(keptn_context, message)
        except Exception as e:
          message.send('`Something went wrong!`')
          logging.error(e)

    except Exception as e:
        logging.error(e)
