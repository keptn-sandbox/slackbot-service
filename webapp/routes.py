from flask import Blueprint

keptn_webserver = Blueprint('keptn_webserver', __name__)

@keptn_webserver.route("/keptnweb")
def hello():
    return "Hello from Keptn Web Server!"