# App Server for Managing Cryptocurrency Assets

![ci pipeline](https://github.com/hoelsch/crypto-assets-server/actions/workflows/pipeline.yml/badge.svg)

Backend Server for [Crypto Assets Management App](https://github.com/hoelsch/crypto-assets-frontend) written in Python using the [Django](https://www.djangoproject.com/) web framework.

## Getting Started: Running the Server Locally

1. Clone this repository:
```sh
git clone https://github.com/hoelsch/crypto-assets-server.git
```

2. Install dependencies
```
python -m pip install -r requirements.txt
```

3. Run database migrations
```
python manage.py migrate
```

4. Initialize database
```
python manage.py loaddata cryptos.json
```

5. Run server
```
python manage.py runserver
```
