from flask import Blueprint
from flask import request
import os
import requests
import json
from slack import WebClient
from flask import Response


keptn_webserver = Blueprint("keptn_webserver", __name__)

SLACK_WEBHOOK = os.getenv("slack_webhook")
SLACK_CHANNEL = os.getenv("slack_channel")
SLACK_BOT_TOKEN = os.getenv("slackbot_token")
slack_client = WebClient(SLACK_BOT_TOKEN)

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

            return "body"
        # validation to check event type
    return "Hello from Keptn Web Server!"

@keptn_webserver.route("/handler", methods=["POST"])
def keptn_approve():
    data = json.loads(request.form["payload"])
    action = data["actions"][0]["value"]
    print(action)

    # based on action approve/reject
    # call keptn API 
    # update message on slack - remove buttons
    
    return Response(status=200)
