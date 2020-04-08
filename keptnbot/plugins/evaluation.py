# -*- coding: utf-8 -*-

from slackbot.bot import respond_to
import re
import json
import requests
import datetime
import os
import time
import logging
import slackbot_settings
import dateutil.parser
import pytz

keptn_host = os.getenv('keptn_host')
keptn_token = os.getenv('keptn_api_token')
headers = {'x-token': keptn_token, 'Content-Type': 'application/json'}

def helper_datetime(mins):
	past = datetime.datetime.now() - datetime.timedelta(minutes=int(mins))
	return past.isoformat()

def convert_iso_to_datetime(s):
	d = dateutil.parser.parse(s)
	return d

def send_event(start, end, project, service, stage):
	
	logging.info(keptn_host)
	#logging.info(keptn_token)

	body = {
  		"data": {
    	"start": start,
    	"end": end,
    	"project": project,
    	"service": service,
    	"stage": stage,
    	"teststrategy": "manual"
  		},
  		"type": "sh.keptn.event.start-evaluation",
			"source": "https://github.com/keptn-sandbox/slackbot-service"
	}
	res = requests.post(url=keptn_host+"/v1/event", headers=headers, data=json.dumps(body), verify=slackbot_settings.TRUST_SELFSIGNED_SSL)
	res_json = res.json()
	logging.info(res_json)
	keptn_context = res_json['keptnContext']
	token = res_json['token']

	return keptn_context

def get_evaluation(keptn_context, message):
	url = '{0}/v1/event?keptnContext={1}&type=sh.keptn.events.evaluation-done'.format(keptn_host, keptn_context)
	
	res_json = None
	
	# 1 minute timeout until status code is 200
	res_timeout = time.time() + slackbot_settings.EVALUATION_TIMEOUT*1 
	while res_timeout > time.time():
		res = requests.get(url=url, headers=headers, verify=slackbot_settings.TRUST_SELFSIGNED_SSL)
		if(res.status_code == 200):
			res_json = res.json()
			break
		time.sleep(1)
	
	# indicator results
	indicators = json.dumps(res_json['data']['evaluationdetails'])
	bridge_url = 'Bridge URL not available'
	if(os.getenv('bridge_url')):
		bridge_url = os.getenv('bridge_url')+'/project/'+res_json['data']['project']
	message.send_webapi("Evaluation-Done", attachments = [
        {
	    "blocks": [
	    	{
	    		"type": "divider"
	    	},
	    	{
	    		"type": "section",
	    		"fields": [
	    			{
	    				"type": "mrkdwn",
	    				"text": "*Project:*\n " + res_json['data']['project']
	    			},
	    			{
	    				"type": "mrkdwn",
	    				"text": "*Service:*\n " + res_json['data']['service']
	    			},
					{
	    				"type": "mrkdwn",
	    				"text": "*Stage:*\n " + res_json['data']['service']
	    			},
					{
	    				"type": "mrkdwn",
	    				"text": "*Strategy:*\n " + res_json['data']['teststrategy']
	    			},
	    			{
	    				"type": "mrkdwn",
	    				"text": "*Time:*\n " + res_json['time']
	    			},
	    			{
	    				"type": "mrkdwn",
	    				"text": "*Result:*\n " + res_json['data']['result']
	    			},
	    			{
	    				"type": "mrkdwn",
	    				"text": "*Keptn Context:*\n " + res_json['shkeptncontext']
	    			},
					{
	    				"type": "mrkdwn",
	    				"text": "*Bridge URL:*\n " + bridge_url
	    			}
	    		]
	    	},
	    	{
	    		"type": "divider"
	    	}
	            ]
        }
    ])
	message.reply(indicators, in_thread=True)

@respond_to(r'start-evaluation (.*)', re.IGNORECASE)
def start_evaluation(message, args):
	try:
		tz_offset = (message.user['tz_offset'])
		user_tz_name = message.user['tz']
		user_tz = pytz.timezone(user_tz_name)
		user_ts = message.body['ts']

		logging.info(user_ts)
		logging.info(tz_offset)
		logging.info(user_tz)
		logging.info(user_tz_name)

		# convert timestamp to datetime
		user_dt = datetime.datetime.fromtimestamp(float(user_ts))

		args_list = args.split(' ')
		# removing empty strings from args list
		args_list = list(filter(None, args_list))
		project, service, stage, start_datetime, end_datetime = '','','','',''


    # start-evaluation sockshop carts preprod 10
		if(len(args_list) == 4):
			project = args_list[0]
			service = args_list[1]
			stage = args_list[2]
			end_datetime_dt = datetime.datetime.fromtimestamp(float(user_ts))
			end_datetime = end_datetime_dt.isoformat()
			start_datetime = (end_datetime_dt - datetime.timedelta(minutes=int(args_list[3]))).isoformat()
			end_datetime = end_datetime+"+00:00"
			start_datetime = start_datetime+"+00:00"

		# start-evaluation sockshop carts preprod 08:00 08:15
		elif(len(args_list) == 5):
			logging.info('evaluation for hours and minutes')
			project = args_list[0]
			service = args_list[1]
			stage = args_list[2]
			
			start_datetime_user = user_dt.isoformat().split('T')[0]+'T'+args_list[3]
			end_datetime_user = user_dt.isoformat().split('T')[0]+'T'+args_list[4]

			unaware_tz_start_dt = convert_iso_to_datetime(start_datetime_user)
			unaware_tz_end_dt = convert_iso_to_datetime(end_datetime_user)

			# set user timezone, convert to UTC and to isoformat
			start_datetime = user_tz.localize(unaware_tz_start_dt.replace(tzinfo=None)).astimezone(pytz.utc).isoformat()
			end_datetime = user_tz.localize(unaware_tz_end_dt.replace(tzinfo=None)).astimezone(pytz.utc).isoformat()
			
		# start-evaluation sockshop carts preprod 20/05/2020 08:00 08:15
		elif(len(args_list) == 6):
			project = args_list[0]
			service = args_list[1]
			stage = args_list[2]
			date = args_list[3] # date in format d/m/y
			start_hour = args_list[4]
			end_hour = args_list[5]
			date_datetime = datetime.datetime.strptime(date, "%d/%m/%Y")
			start_datetime_user = date_datetime.isoformat().split('T')[0]+'T'+args_list[4]+":00.000"
			end_datetime_user = date_datetime.isoformat().split('T')[0]+'T'+args_list[5]+":00.000"
			
			unaware_tz_start_dt = convert_iso_to_datetime(start_datetime_user)
			unaware_tz_end_dt = convert_iso_to_datetime(end_datetime_user)

			# set user timezone, convert to UTC and to isoformat
			start_datetime = user_tz.localize(unaware_tz_start_dt.replace(tzinfo=None)).astimezone(pytz.utc).isoformat()
			end_datetime = user_tz.localize(unaware_tz_end_dt.replace(tzinfo=None)).astimezone(pytz.utc).isoformat()
			
		else:
			now = datetime.datetime.now().isoformat()
			message.reply("`Type in @<myname> help to see what I can do!`")
			return
		
		strategy = 'manual' # args_list[3]

    	# call keptn API send event
		logging.info("Project: " + project)
		logging.info("Service: " + service)
		logging.info("Stage: " + stage)
		logging.info("Strategy: " + strategy)
		logging.info("Start: " + start_datetime)
		logging.info("End: " + end_datetime)
		
		keptn_context = send_event(start_datetime, end_datetime, project, service, stage)

		message.send_webapi("Start-Evaluation", attachments = [
        {
	    "blocks": [
	    	{
	    		"type": "divider"
	    	},
	    	{
	    		"type": "section",
	    		"fields": [
	    			{
	    				"type": "mrkdwn",
	    				"text": "*Project:*\n " + project
	    			},
	    			{
	    				"type": "mrkdwn",
	    				"text": "*Service:*\n " + service
	    			},
					{
	    				"type": "mrkdwn",
	    				"text": "*Stage:*\n " + stage
	    			},
					{
	    				"type": "mrkdwn",
	    				"text": "*Strategy:*\n " + strategy
	    			},
	    			{
	    				"type": "mrkdwn",
	    				"text": "*Start:*\n " + start_datetime
	    			},
	    			{
	    				"type": "mrkdwn",
	    				"text": "*End:*\n " + end_datetime
	    			},
	    			{
	    				"type": "mrkdwn",
	    				"text": "*Keptn Context:*\n " + keptn_context
	    			}
	    		]
	    	},
	    	{
	    		"type": "divider"
	    	}
	            ]
        }
    	])
		
	except Exception as e:
		logging.error(e)

	# loops over until it gets response
	try:
		get_evaluation(keptn_context, message)
	except Exception as e:
		message.send('`Something went wrong!`')
		logging.error(e)