FROM python:3.8.3-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

RUN python manage.py migrate

RUN python manage.py createsuperuser --username admin --password "cswNjgPFaT%pYyU7%N8W9Z^vdud^8nA454vws&XR"

CMD gunicorn --log-level debug --keyfile host.key --certfile host.cert --bind 0.0.0.0:8080 --forwarded-allow-ips "*" Tumble.wsgi