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
```console
echo https://api.keptn.$(kubectl get cm keptn-domain -n keptn -ojsonpath={.data.app_domain})
```
Get the Keptn API token by executing the following command in your terminal:
```console
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

Buid and run the Docker container locally.

```sh
docker build -t DOCKERUSER/slackbot-service:TAG .
```
Run it:

```sh
docker run -d -e slackbot_token=<api token> DOCKERUSER/slackbot-service:TAG
```

Create .env file on the root of this project and set below values
slackbot_token='<slack bot token>'
keptn_host='<keptn host>'
keptn_api_token='<keptn token>'

TODO Example:
slackbot_token=
keptn_host=
keptn_api_token=