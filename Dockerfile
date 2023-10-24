FROM python:3.10-slim

WORKDIR /gdrive

RUN apt-get update && apt-get install -y --fix-missing \
build-essential \
curl \
software-properties-common \
git \
cron \
vim \
&& rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt ./
COPY ./migrate_videos.py ./
COPY ./run.py ./
COPY ./cron-transfer-video.sh ./
COPY ./run-app.sh ./
ADD ./gdrive_app ./gdrive_app

RUN pip install -r requirements.txt

COPY token.json ./
