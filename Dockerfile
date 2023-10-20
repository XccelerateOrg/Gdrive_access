FROM python:3.10-slim

WORKDIR /gdrive

RUN apt-get update && apt-get install -y --fix-missing \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt . && ./migrate_videos.py .
ADD ./gdrive_app .

RUN pip install -r requirements.txt
CMD ["python", "run.py"]


