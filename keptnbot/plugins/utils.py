import time
import datetime
import dateutil.parser
import os
import requests
import logging
import json
import slackbot_settings
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

keptn_host = os.getenv('keptn_host')
keptn_token = os.getenv('keptn_api_token')
headers = {'x-token': keptn_token, 'Content-Type': 'application/json'}


def helper_datetime(mins):
	past = datetime.datetime.now() - datetime.timedelta(minutes=int(mins))
	return past.isoformat()

def convert_iso_to_datetime(s):
	d = dateutil.parser.parse(s)
	return d

def get_evaluation(keptn_context, message):
	url = '{0}/v1/event?keptnContext={1}&type=sh.keptn.events.evaluation-done'.format(keptn_host, keptn_context)
	
	res_json = None
	
	# 1 minute timeout until status code is 200
	res_timeout = time.time() + slackbot_settings.EVALUATION_TIMEOUT*1 
	while res_timeout > time.time():
		res = requests.get(url=url, headers=headers, verify=slackbot_settings.TRUST_SELFSIGNED_SSL)
		logging.info("status code " + str(res.status_code) + " for evaluation-done of keptncontent " + str(keptn_context) + " - retrying...")
		if(res.status_code == 200):
			res_json = res.json()
			break
		time.sleep(5)
	
	# continue with evaluation once we get HTTP200 return code
	indicators = json.dumps(res_json['data']['evaluationdetails'])
	bridge_url = 'Bridge URL not available'
	if(os.getenv('bridge_url')):
		bridge_url = os.getenv('bridge_url')+'trace/'+ str(keptn_context)

	emoji=""
	if (res_json['data']['result'] == "pass"):
		emoji = ":white_check_mark:"
	elif (res_json['data']['result'] == "warning"):
		emoji = ":warning:"
	elif (res_json['data']['result'] == "fail"):
		emoji = ":no_entry:"

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
	    				"text": "*Stage:*\n " + res_json['data']['stage']
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
	    				"text": "*Result:*\n " + res_json['data']['result'] + " " + emoji
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