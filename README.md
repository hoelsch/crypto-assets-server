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

### Run Server in Docker Container

As an alternative, the app can also be executed in a Docker container:

1. Build Docker image
```sh
docker build -t crypto-assets-server .
```

2. Run Docker container
```sh
docker run -p 8000:8000 crypto-assets-server
```

## REST API Documentation

### Register

`POST /register`

#### Body parameters

Name | Type
--- | ---
username | string
email | string
password1 | string
password2 | string

#### Example request

```sh
curl \
  -X POST \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"username":"joe", "email":"joe@doe.com", "password1":"AtEs214derT!", "password2":"AtEs214derT!"}' \
  http://localhost:8000/register
```
#### Example response
```json
{"message":"Successfully created user"}
```

---

### Login

`POST /login`

#### Body parameters

Name | Type
--- | ---
username | string
password | string

#### Example request

```sh
curl \
  -X POST \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"username":"joe", "password":"AtEs214derT!"}' \
  http://localhost:8000/login
```

#### Example response
```json
{"message": "Successfully logged in", "user_id": 1}
```

The response also contains a session cookie in its header.

---

### Logout

`POST /logout`

#### Example request

```sh
curl \
  -X POST \
  http://localhost:8000/logout
```

#### Example response
```json
{"message": "Successfully logged out"}
```

---

### List supported cryptocurrencies

Returns all cryptocurrencies that are supported by the server.

`GET /cryptos`

#### Example request

```sh
curl \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -b 'sessionid=k7dc5nfgjjl1q94iw0atzb14ijsvb4kc' \
  http://localhost:8000/cryptos
```

#### Example response
```json
{
    "cryptos": [
        {
            "name": "bitcoin",
            "abbreviation": "BTC",
            "iconurl": "https://s2.coinmarketcap.com/static/img/coins/64x64/1.png"
        },
        {
            "name": "ethereum",
            "abbreviation": "ETH",
            "iconurl": "https://s2.coinmarketcap.com/static/img/coins/64x64/1027.png"
        },
        {
            "name": "cardano",
            "abbreviation": "ADA",
            "iconurl": "https://s2.coinmarketcap.com/static/img/coins/64x64/2010.png"
        }
    ]
}
```

---

### Get price of cryptocurrency

Returns the current price of a cryptocurrency.

`GET cryptos/<crypto>/price`

#### Example request

```sh
curl \
  -H 'Accept: application/json' \
  -b 'sessionid=k7dc5nfgjjl1q94iw0atzb14ijsvb4kc' \
  http://localhost:8000/cryptos/bitcoin/price
```

#### Example response
```json
{
    "crypto_name": "bitcoin",
    "price": "26643.72000000",
    "unit": "EUR"
}
```

---

### List assets of user

Returns all assets of a user.

`GET /users/<user-id>/assets`

#### Example request

```sh
curl \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -b 'sessionid=k7dc5nfgjjl1q94iw0atzb14ijsvb4kc' \
  http://localhost:8000/users/1/assets
```

#### Example response

```json
{
    "assets": [
        {
            "crypto_name": "bitcoin",
            "user_id": 1,
            "amount": 1.5,
            "abbreviation": "BTC",
            "iconurl": "https://s2.coinmarketcap.com/static/img/coins/64x64/1.png"
        },
        {
            "crypto_name": "ethereum",
            "user_id": 1,
            "amount": 0.5,
            "abbreviation": "ETH",
            "iconurl": "https://s2.coinmarketcap.com/static/img/coins/64x64/1027.png"
        }
    ]
}
```

---

### Create asset for user

An asset represents a specific cryptocurrency and its amount.
If the asset is already existing, its amount will be incremented by the provided amount of the request.

`POST /users/<user-id>/assets/<crypto>`

#### Body parameters

Name | Type
--- | ---
amount | number

#### Example request

```sh
curl \
  -X POST \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -b 'sessionid=k7dc5nfgjjl1q94iw0atzb14ijsvb4kc' \
  -d '{"amount":1.5}' \
  http://localhost:8000/users/1/assets/bitcoin
```

#### Example response

```json
{
    "message": "Successfully added 1.5 bitcoin to assets",
    "crypto": "bitcoin",
    "new_amount": 3.0
}
```

### Replace asset for user

Replaces the amount of an existing asset with the amount provided in the request.
If the asset does not exist, it will be created.

`PUT /users/<user-id>/assets/<crypto>`

#### Body parameters

Name | Type
--- | ---
amount | number

#### Example request

```sh
curl \
  -X PUT \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -b 'sessionid=k7dc5nfgjjl1q94iw0atzb14ijsvb4kc' \
  -d '{"amount":1}' \
  http://localhost:8000/users/1/assets/bitcoin
```

#### Example response

```json
{
    "message": "Successfully added 1.0 bitcoin to assets",
    "crypto": "bitcoin",
    "new_amount": 1.0
}
```

---

### Delete asset of user

`DELETE /users/<user-id>/assets/<crypto>`

#### Example request

```sh
curl \
  -X DELETE \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -b 'sessionid=k7dc5nfgjjl1q94iw0atzb14ijsvb4kc' \
  http://localhost:8000/users/1/assets/bitcoin
```

#### Example response

```json
{"message": "Successfully deleted asset bitcoin"}
```
