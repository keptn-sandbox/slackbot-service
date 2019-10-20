FROM python:3

# copy files to /pp directory
COPY . /app

WORKDIR /app

# install app dependencies
RUN pip install -r requirements.txt

ENV slackbot_token=

ENTRYPOINT ["python"]
CMD ["run.py"]
