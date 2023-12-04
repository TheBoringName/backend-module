FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/backend-module:/backend-module/web
ENV FLASK_APP=app
RUN apt-get update && apt-get install -y ffmpeg
RUN pip install --upgrade pip

RUN mkdir /backend-module
WORKDIR /backend-module
COPY requirements.txt /backend-module
RUN pip install -r requirements.txt

COPY . /backend-module



CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
