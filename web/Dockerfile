FROM python:3.8.3-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG BANKSPREAD_VERSION
ARG STARLING_CLIENT_SECRET
ARG DJANGO_SECRET_KEY

ENV BANKSPREAD_VERSION=$BANKSPREAD_VERSION
ENV STARLING_CLIENT_SECRET=$STARLING_CLIENT_SECRET
ENV DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY
ENV DJANGO_SETTINGS_MODULE=Tumble.settings.production

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

RUN python manage.py makemigrations

RUN python manage.py migrate

CMD gunicorn --log-level debug --bind 0.0.0.0:8080 --forwarded-allow-ips "*" Tumble.wsgi