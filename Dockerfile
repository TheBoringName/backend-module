FROM ubuntu:20.04

ARG TZ=Europe/Warsaw
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


RUN apt-get update && apt-get install -y \
    python3.8 \
    python3-pip \
    ffmpeg \
    vim \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

RUN wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | apt-key add -
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list
RUN apt-get update && apt-get install -y mongodb-org
RUN systemctl enable mongod

WORKDIR /app

COPY . /app/

RUN pip3 install -r requirements.txt

CMD ["python3", "functions/session.py"]