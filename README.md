# Slackbot service

![GitHub release (latest by date)](https://img.shields.io/github/v/release/keptn-contrib/slackbot-service?include_prereleases)

The *slackbot-service* is a [Keptn](https://keptn.sh) service that is responsible for interacting with Keptn via a Slack bot. You can interact with the bot by e.g., asking for a deployment evaluation.

The service itself doesn't have to run in the Keptn cluster, however, it is for sure possible. 


## Installation

### Create bot user in Slack and receive bot token


1. Go to https://YOUR-SLACK-TENANT.slack.com/apps/manage/custom-integrations and click on Bots to add a bot user.
    ![botuser](./images/bot-user.png)

1. Click on **Add to Slack** and give your bot a username. This will be the name you will interact with the bot. A good name would be, e.g., **keptn**

1. Click on **Add bot integration**

1. In the next screen you will see the API Token for your Bot user. You will need this token to connect your Slackbot-Service with the just created bot.
    You can also change the name here, or customize the bot by changing the icon.
    ![bot-token](./images/bot-token.png)

<!--
alternative way

1. Create Slack app

    https://api.slack.com/apps?new_app=1

1.
-->


### Get credentials

**Slack**

You will need the Slack Bot token you received during the setup of the Bot user.

**Keptn**

Get the Keptn endpoint by executing the following command in your terminal:
```sh
echo https://api.keptn.$(kubectl get cm keptn-domain -n keptn -ojsonpath={.data.app_domain})
```
Get the Keptn API token by executing the following command in your terminal:
```sh
echo $(kubectl get secret keptn-api-token -n keptn -ojsonpath={.data.keptn-api-token} | base64 --decode)
```

### Set environment variables

Clone the repo or download just the `deploy/slackbot-service.yaml` file.
Edit the `env` section of the file to have the environment variables match your Keptn API token and Slackbot Token.
If you are going to deploy the Slackbot service into the Keptn cluster, you can keep the default for the variable `KEPTN_HOST`. If you are going to deploy it on a different cluster, please update the KEPTN_HOST to point to your cluster.
```yaml
env:
- name: keptn_host
  value: "http://api.keptn.svc.cluster.local"
- name: keptn_api_token
  value: ""
- name: slackbot_token
  value: ""
```


### Compatibility Matrix

Please always double check the version of Keptn you are using compared to the version of this service, and follow the compatibility matrix below.


| Keptn Version    | [Slackbot Service Image](https://hub.docker.com/r/keptncontrib/slackbot-service/tags) |
|:----------------:|:----------------------------------------:|
|       0.6.x      | keptncontrib/slackbot-service:0.1.0  |


## Local development

### Python Virtual Environment

1. If not installed yet install the `virtualenv` for your python installation with:

    ```console
    pip install virtualenv
    ```

1. Within your `slackbot-service` folder create the virtual environment with: 

    ```console
    virtualenv venv
    ```

1. Active the virtual environment: 

    ```console
    source venv/bin/active
    ```

1. Install the requirements into the virtual environment:

    ```console
    pip install -r requirements.txt
    ```

1. Make sure you have the credentials defined in a `.env` file in the project directory:

    ```
    slackbot_token='xxx'
    keptn_host='https://api.keptn.YOUR-IP.com'
    keptn_api_token='xxx'
    ```

1. Run the Slackbot:

    ```console
    python run.py
    ```

### Docker Build

Buid and run the Docker container locally.

```sh
docker build -t DOCKERUSER/slackbot-service:TAG .
```
Run it:

```sh
docker run -d -e slackbot_token=<api token> DOCKERUSER/slackbot-service:TAG
```

Create .env file on the root of this project and set below values
```
slackbot_token='<slack bot token>'
keptn_host='<keptn host>'
keptn_api_token='<keptn token>'
 ```


Example:
```
slackbot_token='xoxb-abcdef-abcdef'
keptn_host='https://api.keptn.123.45.67.890.xip.io'
keptn_api_token='xcfaaefoobar'
```
---


**Thanks** to James Tatum & lins05  for developing slackbot library [pypi-slackbot](https://pypi.org/project/slackbot/)

