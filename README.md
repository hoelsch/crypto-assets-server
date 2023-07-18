# App Server for Managing Cryptocurrency Assets

![ci pipeline](https://github.com/hoelsch/crypto-assets-server/actions/workflows/pipeline.yml/badge.svg)

Backend Server for [Crypto Assets Management App](https://github.com/hoelsch/crypto-assets-frontend) written in Python using the [Django](https://www.djangoproject.com/) web framework.

## Getting Started: Running the Server Locally

1. Clone this repository:
```sh
git clone https://github.com/hoelsch/crypto-assets-server.git
```

2. Install dependencies
```sh
python -m pip install -r requirements.txt
```

3. Create database schema
```sh
python manage.py migrate
```

4. Initialize database
```sh
python manage.py loaddata cryptos.json
```

5. Run server
```sh
python manage.py runserver
```

## Run Server in Docker Container

As an alternative, the app can also be executed in a Docker container:

1. Build Docker image
```sh
docker build -t crypto-assets-server .
```

2. Run Docker container
```sh
docker run -p 8000:8000 crypto-assets-server
```
