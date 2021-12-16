FROM python:3.10.1-slim
RUN apt-get update && apt-get install -y wait-for-it
COPY requirements.txt requirements.txt
COPY main.py main.py
COPY discord_webhook_client.py discord_webhook_client.py
RUN pip3 install -r requirements.txt
