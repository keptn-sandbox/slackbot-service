# Slackbot service

![GitHub release (latest by date)](https://img.shields.io/github/v/release/keptn-contrib/slackbot-service?include_prereleases)

The *slackbot-service* is a [Keptn](https://keptn.sh) service that is responsible for interacting with Keptn via a Slack bot.

The service itself doesn't have to run in the Keptn cluster, however, it is for sure possible. 


## Installation

### Provide credentials

**Slack**

TODO: 
Provide instructions how to setup Slack and how to get the token that is needed

**Keptn**

Get the Keptn endpoint by executing the following command in your terminal:
```sh
echo https://api.keptn.$(kubectl get cm keptn-domain -n keptn -ojsonpath={.data.app_domain})
```
Get the Keptn API token by executing the following command in your terminal:
```sh
echo $(kubectl get secret keptn-api-token -n keptn -ojsonpath={.data.keptn-api-token} | base64 --decode)
```

### Enter crededentials

TODO

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

1. Make sure you have the credentials defined in a `.env` file:

    ```
    slackbot_token='xxx'
    keptn_host='https://api.keptn.YOURIP.com'
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


TODO Example:
```
slackbot_token=''
keptn_host='https://api.keptn.123.45.67.890.xip.io'
keptn_api_token='xcfaaefoobar'
```
