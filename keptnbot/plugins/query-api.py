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
      myprojects = ""
      for project in res_json['projects']:
        logging.info("project: " + project['projectName'])
        logging.info(project)
        logging.info("")
        myprojects = myprojects + "\n • " + project['projectName']
        # for stage in project['stages']:
        #   logging.info("stage: ")
        #   logging.info(stage)

      if myprojects != "":
        myprojects = "Here is the list of projects:\n" + myprojects
        myprojects = myprojects + "\n You can ask for the services of each project with @Keptn get services of <projectname>"
      else:
        myprojects = "No projects found."

      message.send_webapi(myprojects)


    except Exception as e:
      message.send('`Something went wrong!`')
      logging.error(e)

# get projects
@respond_to(r'get services of (.*)', re.IGNORECASE)
def get_services(message, args):
    try:
      projectname = args.strip()

      url = '{0}/configuration-service/v1/project/?pageSize=50'.format(utils.keptn_host)
      # https://api.keptn.xxx.xip.io/configuration-service/v1/project?pageSize=20&disableUpstreamSync=false
      res = requests.get(url=url, headers=utils.headers, verify=slackbot_settings.TRUST_SELFSIGNED_SSL)
      logging.info("status code " + str(res.status_code) + " for getting projects")
      logging.info(res.content)

      res_json = res.json()
      logging.info(res_json)
      myservices = ""
      for project in res_json['projects']:
        logging.info("project: " + project['projectName'])
        logging.info(project)
        logging.info("")
        if project['projectName'] == projectname:
          stage = project['stages'][0]
          stagename = stage['stageName']
          logging.info("stage: " + stagename)
          url = '{0}/configuration-service/v1/project/{1}/stage/{2}/service?pageSize=50'.format(utils.keptn_host, projectname, stagename)
          res = requests.get(url=url, headers=utils.headers, verify=slackbot_settings.TRUST_SELFSIGNED_SSL)
          res_json = res.json()
          logging.info(res_json)
          for service in res_json['services']:
            logging.info(service)
            myservices = myservices + "\n • " + service['serviceName']

      if myservices != "":
        myservices = "Here is the list of services in project "+projectname+":\n" + myservices
      else:
        myservices = "No services found."

      message.send_webapi(myservices)


    except Exception as e:
      message.send('`Something went wrong!`')
      logging.error(e)
