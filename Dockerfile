FROM ubuntu:20.04

ARG TZ=Europe/Warsaw
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y \
    python3.8 \
    python3-pip \
    ffmpeg \
    vim \
    gnupg \
    wget \
    systemctl \
    && rm -rf /var/lib/apt/lists/*

RUN wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | apt-key add -
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list
RUN apt-get update && apt-get install -y mongodb-org
RUN systemctl enable mongod


FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/backend-module:/backend-module/web
ENV FLASK_APP=app

COPY . /backend-module

WORKDIR /backend-module

RUN pip install --upgrade pip
RUN pip install -r requirements.txt 

WORKDIR /pwse/backend

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
# # CMD ["python3", "functions/session.py"]