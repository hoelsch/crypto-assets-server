FROM python:3.11-alpine3.18
COPY . /app
WORKDIR /app
RUN python -m pip install -r requirements.txt
RUN python manage.py migrate
RUN python manage.py loaddata cryptos.json
CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "crypto_assets_server.wsgi"]
