# Basic message API

API built with FastAPI and SQLAlchemy, deployed on heroku.

# Dependencies

```
FastAPI uvicorn SQLAlchemy
```

# Deployment

API deployed on heroku with GitHub automatic deploy.
If you want to run it locally use:
`uvicorn app.main:app --reload`

# Authorization

API uses `api_key` to authorize requests. All unauthorized requests will be rejected and will return `HTTP 403 Forbidden`.
There are 3 ways to pass `api_key`:

1. As query string `?api_key={ApiKey}`

```bash
curl -X 'POST' \
  'https://basic-message-api.herokuapp.com/message?api_key=helloworld' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "hello world"
}'
```

2. In the cookie `api_key`.

```bash
curl -X 'PATCH' \
  'https://basic-message-api.herokuapp.com/message/1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Cookie: api_key=helloworld' \
  -d '{
  "text": "bye world"
}'
```

3. In the header `api_key`.

```bash
curl -X 'GET' \
  'http://basic-message-api.herokuapp.com/message/1' \
  -H 'accept: application/json' \
  -H 'api_key: helloworld'
```

# /message endpoint

Endpoint responsible for creating, updating, deleting and fetching messages depending on the HTTP method. It uses `MessageRequest` and `MessageResponse` classes written in pydantic for validating data and returning responses.

## MessageRequest

Simple model used for creating and updating saved messages.

```json
{
  "text": "message body"
}
```

## MessageResponse

Model responsible for returning saved messages data.

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

### Example

```bash
curl -X 'POST' \
  'http://basic-message-api.herokuapp.com/message' \
  -H 'accept: application/json' \
  -H 'api_key: helloworld' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "message body"
}'
```

## PATCH `/message/{message_id}`

`https://basic-message-api.herokuapp.com/message/{message_id}`

Updates message's text value with new one passed in `MessageRequest` and resets counter to 0. Returns `MessageResponse`.

```json
{
  "id": 1,
  "text": "new message body",
  "counter": 0
}
```

### Example

```bash
curl -X 'PATCH' \
  'http://basic-message-api.herokuapp.com/message/1' \
  -H 'accept: application/json' \
  -H 'api_key: helloworld' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "new message body"
}'
```

## DELETE `/message/{message_id}`

`https://basic-message-api.herokuapp.com/message/{message_id}`

Deletes message with id `{message_id}`. If message with passed id does not exist `HTTP 404 Not Found` is returned.

```json
{
  "deleted_message_id": 1
}
```

### Example

```bash
curl -X 'DELETE' \
  'http://basic-message-api.herokuapp.com/message/1' \
  -H 'accept: application/json' \
  -H 'api_key: helloworld'
```

## GET `/message/{message_id}`

`https://basic-message-api.herokuapp.com/message/{message_id}`

Fetches message with id `{message_id}` if exists, else returns `HTTP 404 Not Found`. With every GET request increments counter by 1.

```json
{
  "id": 1,
  "text": "message body",
  "counter": 1
}
```

### Example

```bash
curl -X 'GET' \
  'http://basic-message-api.herokuapp.com/message/1' \
  -H 'accept: application/json' \
  -H 'api_key: helloworld'
```
