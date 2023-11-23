FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/backend-module:/backend-module/web
ENV FLASK_APP=app

COPY . /backend-module

WORKDIR /backend-module

RUN pip install --upgrade pip
RUN pip install -r requirements.txt 

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]