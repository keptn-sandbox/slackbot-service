from flask import Blueprint
from flask import request
import os
import requests
import json
from slack import WebClient
from flask import Response
import pickle
import logging
import slackbot_settings

keptn_webserver = Blueprint("keptn_webserver", __name__)

SLACK_WEBHOOK = os.getenv("slack_webhook")
SLACK_CHANNEL = os.getenv("slack_channel")
SLACK_BOT_TOKEN = os.getenv("slackbot_token")
slack_client = WebClient(SLACK_BOT_TOKEN)

keptn_host = os.getenv('keptn_host')
keptn_token = os.getenv('keptn_api_token')
headers = {'x-token': keptn_token, 'Content-Type': 'application/json'}
bridge_url = os.getenv('bridge_url')

def save_request(data):
    req_obj = {}
    req_obj[data["triggeredid"]] = data
    #print(req_obj)
    req_file = open(keptn_webserver.root_path+"/data/"+ data["triggeredid"], "wb")
    pickle.dump(req_obj, req_file)
    req_file.close()

def load_request(id):
    req_file = open(keptn_webserver.root_path+"/data/"+id, 'rb')      
    req_obj = pickle.load(req_file)
    #print(req_obj)
    req_file.close()
    return req_obj 

@keptn_webserver.route("/", methods=["GET","POST"])
def keptn_approval():
    if(request.method == 'POST'):
        
        data = request.get_json()
        if(data["type"] == "sh.keptn.event.approval.triggered"):
            # post to slack
            approval_message = slack_client.chat_postMessage(
            channel=SLACK_CHANNEL,
            #text="Approval awaiting action.",
                attachments=[
                    {
                        "fields": [
                            {
                                "title": "Project",
                                "value": data["data"]["project"],
                                "short": True
                            },
                            {
                                "title": "Stage",
                                "value": data["data"]["stage"],
                                "short": True
                            },
                            {
                                "title": "Service",
                                "value": data["data"]["service"],
                                "short": True
                            },
                            {
                                "title": "Result",
                                "value": data["data"]["result"],
                                "short": True
                            },
                            {
                                "title": "Image",
                                "value": data["data"]["image"],
                                "short": True
                            },
                            {
                                "title": "Time",
                                "value": data["time"],
                                "short": True
                            },
                            {
                                "title": "Keptn Context",
                                "value": data["shkeptncontext"],
                                "short": True
                            },
                            {
                                "title": "Triggered ID",
                                "value": data["triggeredid"],
                                "short": True
                            },
                            {
                                "title": "Event Type",
                                "value": data["type"],
                                "short": True
                            }
                        ],
                        "title": "Title",
                        "color": "#FF0000",
                        "text": "Approval awaiting action",
                    },
                    {
                        "text": "",
                                "callback_id": "approval_req",
                                "attachment_type": "default",
                                "actions": [
                                    {
                                        "name": "approval_pass",
                                        "text": "Approve :heavy_check_mark:",
                                        "type": "button",
                                        "value": "approval_pass"
                                    },
                                    {
                                        "name": "approval_fail",
                                        "text": "Reject :x:",
                                        "type": "button",
                                        "value": "approval_fail"
                                    }
                                ]
                    }
                ]
            )
            
            # use pickle to store request json object
            # access request object from handler function
            # when sending trigger finish event
            # since request object can get big it's feasible to access from slack message
            # and we can display only neccessary fields to the user in slack

            save_request(data)

            return Response(status=200)

    return "Hello from Keptn Bot!"

@keptn_webserver.route("/handler", methods=["POST"])
def keptn_approve():
    data = json.loads(request.form["payload"])
    action = data["actions"][0]["value"]
    
    # read triggerid from slack message to access request object for it
    # make sure trigger_id field is second last in slack message
    triggered_id = data["original_message"]["attachments"][0]["fields"][-2]['value']
    request_obj = load_request(triggered_id)
    #print(request_obj)
    
    # return 200 and func continue 
    Response(status=200)

    # based on action approve/reject
    # call keptn event API 
    # update message on slack - remove buttons
    print(action)
    body = request_obj[triggered_id]
    # remove dict keys that are not needed
    print(body)
    del body["id"]
    del body["time"]
    del body["data"]["result"]

    # construct approval object
    approval = {}
    if(action == "approval_pass"):
        body["data"]["approval"] = {"result":"pass", "status":"succeeded"}

    body["data"]["approval"] = {"result":"failed", "status":"succeeded"}
    print(body)
    res = requests.post(url=keptn_host+"/v1/event", headers=headers, data=json.dumps(body), verify=slackbot_settings.TRUST_SELFSIGNED_SSL)
    res_json = res.json()
    logging.info(res_json)
    
    return Response(status=200)
