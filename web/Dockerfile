FROM python=3.8.3-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG STARLING_CLIENT_ID
ARG STARLING_CLIENT_SECRET
ARG STARLING_REDIRECT_URL
ARG STARLING_API_URL
ARG STARLING_BASE_URL
ARG STARLING_OAUTH_URL
ARG GOOGLE_REDIRECT_URL
ARG SECRET_KEY

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

RUN python manage.py makemigrations

RUN python manage.py migrate

CMD gunicorn --log-level debug --bind 0.0.0.0=8080 --forwarded-allow-ips "*" Tumble.wsgi