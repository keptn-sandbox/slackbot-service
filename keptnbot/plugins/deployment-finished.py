# -*- coding: utf-8 -*-

from slackbot.bot import respond_to
import re
import json
import os
import logging
import requests
import slackbot_settings

keptn_host = os.getenv('keptn_host')
keptn_token = os.getenv('keptn_api_token')
headers = {'x-token': keptn_token, 'Content-Type': 'application/json'}

def send_event(project, service, stage, strategy, deployment_uri):
    body = {
      "type": "sh.keptn.events.deployment-finished",
      "specversion": "0.2",
      "source": "https://github.com/keptn-sandbox/slackbot-service",
      "contenttype": "application/json",
      "data": {
        "project": "simpleproject",
        "stage": "performance",
        "service": "simplenode",
        "testStrategy": "performance",
        "labels": {
          "runby": "KeptnBot"
        },
        "deploymentURI": "http://simplenode.simpleproject-performance.35.239.209.123.xip.io/"
      }
    }

    res = requests.post(url=keptn_host+"/v1/event", headers=headers, data=json.dumps(body), verify=slackbot_settings.TRUST_SELFSIGNED_SSL)
    res_json = res.json()
    logging.info(res_json)
    keptn_context = res_json['keptnContext']
    token = res_json['token']
    
    return keptn_context

@respond_to(r'deployment-finished (.*)', re.IGNORECASE)
def deployment_finished(message, args):
    try:
        args_list = args.split(' ')
        
        # removing empty strings from args list
        args_list = list(filter(None, args_list))
        logging.info(args_list)
        project, service, stage, strategy, deployment_uri = '','','','',''

        if(len(args_list) != 5):
            message.reply("`Incorrect number of arguments!`")
            return
        
        keptn_context = send_event(project, service, stage, strategy, deployment_uri)
        logging.info(keptn_context)

    except Exception as e:
        logging.error(e)
