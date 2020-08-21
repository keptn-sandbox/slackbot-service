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
import time

keptn_webserver = Blueprint("keptn_webserver", __name__)

SLACK_CHANNEL = os.getenv("slack_channel")
SLACK_BOT_TOKEN = os.getenv("slackbot_token")

slack_client = WebClient(SLACK_BOT_TOKEN)

keptn_host = os.getenv('keptn_host')
keptn_token = os.getenv('keptn_api_token')
headers = {'x-token': keptn_token, 'Content-Type': 'application/json'}
bridge_url = os.getenv('bridge_url')

def get_bridge_url(trace):
    if bridge_url.endswith("/"):
        return bridge_url + "trace/" + trace
    return bridge_url + "/trace/" + trace

def save_request(data):
    req_obj = {}
    req_obj[data["triggeredid"]] = data
    #print(req_obj)
    #req_file = open(keptn_webserver.root_path+"/data/"+ data["triggeredid"], "wb")
    req_file = open(data["triggeredid"], "wb")
    pickle.dump(req_obj, req_file)
    req_file.close()

def load_request(id):
    req_file = open(id, 'rb')      
    req_obj = pickle.load(req_file)
    #print(req_obj)
    req_file.close()
    return req_obj 

@keptn_webserver.route("/", methods=["GET","POST"])
def keptn_approval():
    if(request.method == 'POST'):
        data = request.get_json()
        triggered_id = data["id"]
        project = data["data"]["project"]
        stage = data["data"]["stage"]
        service = data["data"]["service"]
        data["triggeredid"] = triggered_id
        bridgelink=""
        if (str(bridge_url) != ""):
            bridgelink = "Find details <"+ get_bridge_url(str(data["shkeptncontext"]))+"|in the bridge>."

        if(data["type"] == "sh.keptn.event.approval.triggered"):

            # make an api call to validate if approval still exist
            
            # 3 seconds wait before checking if approval request exist
            time.sleep(3)
            approval_url = "{0}/api/configuration-service/v1/project/{1}/stage/{2}/service/{3}/approval/{4}?pageSize=20"\
                .format(keptn_host, project, stage, service, triggered_id)
            
            req_approval_exist = requests.get(url=approval_url, headers={"x-token":keptn_token})
            if(req_approval_exist.status_code != 200):
                logging.info("Status code: {0} from url: {1}".format(str(req_approval_exist.status_code), approval_url))
                logging.info("Function abort - approval request will only posted to slack if approval exist - return status 200")
                return Response(status=200)
            
            # post to slack
            approval_message = slack_client.chat_postMessage(
            channel=SLACK_CHANNEL,
            #text="Approval awaiting action.",
                attachments=[
                    {
                        "fields": [
                            {
                                "title": "Project",
                                "value": project,
                                "short": True
                            },
                            {
                                "title": "Stage",
                                "value": stage,
                                "short": True
                            },
                            {
                                "title": "Service",
                                "value": service,
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
                                "title": "Bridge Link",
                                "value": bridgelink,
                                "short": True
                            },
                            {
                                "title": "Keptn Context",
                                "value": data["shkeptncontext"],
                                "short": True
                            },
                            {
                                "title": "Triggered ID",
                                "value": triggered_id,
                                "short": True
                            },
                            {
                                "title": "Event Type",
                                "value": data["type"],
                                "short": True
                            }
                        ],
                        "title": "You have a new approval request:",
                        "color": "#FF0000",
                        #"text": "Approval awaiting action",
                    },
                    {
                        "text": "",
                                "callback_id": "approval_req",
                                "attachment_type": "default",
                                "actions": [
                                    {
                                        "name": "approval_pass",
                                        "text": "Approve",
                                        "type": "button",
                                        "style": "primary",
                                        "value": "approval_pass"
                                    },
                                    {
                                        "name": "approval_fail",
                                        "text": "Reject",
                                        "type": "button",
                                        "style": "danger",
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
    message_ts = data["message_ts"]

    # read triggerid from slack message to access request object for it
    # make sure trigger_id field is second last in slack message
    triggered_id = data["original_message"]["attachments"][0]["fields"][-2]['value']
    request_obj = load_request(triggered_id)
    
    # return 200 and func continue 
    Response(status=200)

    # based on action approve/reject
    # call keptn event API 
    # update message on slack - remove buttons
    #print(action)
    body = request_obj[triggered_id]
    # remove dict keys that are not needed
    #print(body)
    del body["id"]
    del body["time"]
    del body["data"]["result"]
    body["type"] = "sh.keptn.event.approval.finished"

    # construct approval object
    approval = {}
    logging.info("Approval Request: {}".format(str(action)))
    body["data"]["approval"] = {"result":"failed", "status":"succeeded"}
    approval_result = ("Rejected :x:", "")

    if(action == "approval_pass"):
        body["data"]["approval"] = {"result":"pass", "status":"succeeded"}
        approval_result = ("Approved :heavy_check_mark:", "#008000")

    #print(body)
    logging.info("keptnURL: " + keptn_host+"/api/v1/event")
    res = requests.post(url=keptn_host+"/api/v1/event", headers=headers, data=json.dumps(body), verify=slackbot_settings.TRUST_SELFSIGNED_SSL)
    #res_json = res.json()
    logging.info(res.content)
    
    if(res.status_code != 200):
        logging.error("Could not get HTTP 200 response from Keptn: " + str(res.status_code))
        return

    bridgelink=""
    if (str(bridge_url) != ""):
        bridgelink = "Find details <"+ get_bridge_url(str(body["shkeptncontext"]))+"|in the bridge>."
        
    # update slack message and remove buttons
    approval_message = slack_client.chat_update(
            channel=SLACK_CHANNEL,
            ts=message_ts,
            #text="Approval awaiting action.",
                attachments=[
                    {
                        "fields": [
                            {
                                "title": "Project",
                                "value": body["data"]["project"],
                                "short": True
                            },
                            {
                                "title": "Stage",
                                "value": body["data"]["stage"],
                                "short": True
                            },
                            {
                                "title": "Service",
                                "value": body["data"]["service"],
                                "short": True
                            },
                            {
                                "title": "Image",
                                "value": body["data"]["image"],
                                "short": True
                            },
                            {
                                "title": "Bridge Link",
                                "value": bridgelink,
                                "short": True
                            },
                            {
                                "title": "Keptn Context",
                                "value": body["shkeptncontext"],
                                "short": True
                            },
                            {
                                "title": "Triggered ID",
                                "value": body["triggeredid"],
                                "short": True
                            },
                            {
                                "title": "Event Type",
                                "value": body["type"],
                                "short": True
                            }
                        ],
                        "title": "Approval Request: {}".format(approval_result[0]),
                        "color": approval_result[1],
                        #"text": "Approval awaiting action",
                    }
                ]
            )
    
    return Response(status=200)
