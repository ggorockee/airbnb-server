# docker
FROM python:3.11.9
RUN apt-get -y update
COPY app /app
COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt
WORKDIR /app

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8080" ]