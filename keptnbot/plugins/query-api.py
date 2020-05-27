# -*- coding: utf-8 -*-

from slackbot.bot import respond_to
import re
import logging
import os
import json
import requests
import slackbot_settings
from keptnbot.plugins import utils


# get projects
@respond_to(r'get projects', re.IGNORECASE)
def get_projects(message):
    try:
      url = '{0}/configuration-service/v1/project?pageSize=50'.format(utils.keptn_host)
      # https://api.keptn.xxx.xip.io/configuration-service/v1/project?pageSize=20&disableUpstreamSync=false
      res = requests.get(url=url, headers=utils.headers, verify=slackbot_settings.TRUST_SELFSIGNED_SSL)
      logging.info("status code " + str(res.status_code) + " for getting projects")
      logging.info(res.content)

      res_json = res.json()
      logging.info(res_json)
      for project in res_json['projects']:
        logging.info(project)
        for stage in project['stages']:
          logging.info(stage)

      


    except Exception as e:
      message.send('`Something went wrong!`')
      logging.error(e)
