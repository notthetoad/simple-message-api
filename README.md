# Simple message API

API built with FastAPI and SQLAlchemy, deployed on heroku.

# Dependencies

> FastAPI uvicorn SQLAlchemy

# Deployment

API deployed on heroku with GitHub automatic deploy.

# Authorization

API uses `api_key` to authorize requests. All unauthorized requests will be rejected and will return `HTTP 403 Forbidden`.
There are 3 ways to pass `api_key`:

1. As query string `?api_key={ApiKey}`

```
curl -X 'POST' \
  'https://simple-message-api.herokuapp.com/message?api_key=helloworld' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "hello world"
}'
```

2. In the cookie `api_key`.

```
curl -X 'PATCH' \
  'https://simple-message-api.herokuapp.com/message/1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Cookie: api_key=helloworld' \
  -d '{
  "text": "bye world"
}'
```

3. In the header `api_key`.

```
curl -X 'GET' \
  'http://127.0.0.1:8000/message/1' \
  -H 'accept: application/json' \
  -H 'api_key: helloworld'
```

# /message endpoint

Endpoint responsible for creating, updating, deleting, and fetching messages depending on the HTTP method. It uses `MessageRequest` and `MessageResponse` classes written in pydantic for validating data, and returning responses.

## MessageRequest

Simple model used for creating and updating saved messages.

```json
{
  "text": "message body"
}
```

## MessageResponse

```json
{
  "id": 1,
  "text": "message body",
  "counter": 2
}
```

## POST `/message`

`https://basic-message-api.herokuapp.com/message`

Receives `MessageRequest` and returns json containing saved message's id and text like so:

```json
{
  "id": 1,
  "text": "hello world"
}
```

## PATCH `/message/{message_id}`

`https://basic-message-api.herokuapp.com/message/{message_id}`

Updates message's text value with new one passed in `MessageRequest` and resets counter to 0. Returns id, updated text and reset counter.

```json
{
  "id": 1,
  "text": "new message body",
  "counter": 0
}
```

## DELETE `/message/{message_id}`

`https://basic-message-api.herokuapp.com/message/{message_id}`

Deletes message of `{message_id}`. If message of passed id does not exist, API returns `HTTP 404 Not Found`.

```json
{
  "deleted message id": 1
}
```

## GET `/message/{message_id}

`https://basic-message-api.herokuapp.com/message/{message_id}`

Fetches message of `{message_id}`. With every GET request incements counter by 1. If message of passed id does not exist, API returns `HTTP 404 Not Found`.

```json
{
  "id": 1,
  "text": "message body",
  "counter": 1
}
```
