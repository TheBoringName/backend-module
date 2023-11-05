FROM ubuntu:20.04

ARG TZ=Europe/Warsaw
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


RUN apt-get update && apt-get install -y \
    python3.8 \
    python3-pip \
    ffmpeg \
    vim \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app/

RUN pip3 install -r requirements.txt

CMD ["python3", "functions/session.py"]