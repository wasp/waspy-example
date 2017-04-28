# Endpoints
endpoint references are in HTTPie syntax

## ping
this endpoint is the most basic endpoint. It just responds to a ping. 
It is a GET endpoint, and doesnt support any parameters.

```bash
$ http -v :8080/ping
HTTP/1.1 200 OK
content-length: 19
content-type: application/json
server: foo-service

{
    "result": "pong "
}
```

## echo
There are two echo endpoints. 
### GET 
The GET just responds with all the things it received
such as the query and headers.

```bash
$ http -v :8080/echo foo==bar foo==baz cabbage==green
GET /echo?foo=bar&foo=baz&cabbage=green HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:8080
User-Agent: HTTPie/0.9.9


HTTP/1.1 200 OK
content-length: 271
content-type: application/json
server: foo-service

{
    "headers": {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate",
        "connection": "keep-alive",
        "host": "localhost:8080",
        "user-agent": "HTTPie/0.9.9"
    },
    "query": {
        "cabbage": [
            "green"
        ],
        "foo": [
            "bar",
            "baz"
        ]
    },
    "query_string": "foo=bar&foo=baz&cabbage=green",
    "url": "/echo"
}
```

### POST
The post endpoint just echo's the body. 

```
$ http :8080/echo foo=bar
```

response:
```json
{
    "foo": "bar"
}
```


## error
This endpoint returns an error. It is a GET request that accepts an `error_code` query parameter.
If `error_code` is not defined, a 400 will be returned.
 
```bash
$ http -v :8080/error error_code==500
```

response looks like:

```json
{
    "code": 500,
    "message": "here is a message"
}
```

## callback
This endpoint calls another service and wait for it to respond before responding.
It is a POST and excepts the following items (all are optional except for the path):
The service name is optional, as you could have service discovery (the default rabbit implementation)

* *service*: the name of the service you are calling. (optional if you have service discovery)
* *path*: the url path (required)
* *method*: method used to call the service (GET,POST,PATCH,etc.)
* *body*: the body to send to the service

## foo
This endpoint tries to mimic a typical REST endpoint. It contains a GET, PUT, POST, PATCH, and DELETE.
*Note:* there is no database for this example, so all results are hard coded. You cant actually create/delete
real resources

### POST
Use the `/foo` path and pass any body. The response will be a foo object, with the id 25 and your body
as if it was part of the object.

```bash
$ http POST :8080/foo hello=world foo=bar
HTTP/1.1 201 Created
content-length: 51
content-type: application/json
server: foo-service

{
  "foo": {
      "foo": "bar",
      "hello": "world",
      "id": 25
  }
}
```

### GET
Get a foo. Url is of pattern `/foo/:id` where id is the fooid.

```bash
$ http :8080/foo/10
HTTP/1.1 200 OK
content-length: 35
content-type: application/json
server: foo-service

{
    "foo": {
        "bar": "baz",
        "id": "10"
    }
}
```

### PUT
edit a foo. Url is of pattern `/foo/:id` where id is the fooid.
This url will only work if you use the id 25, otherwise you will get a 404.
You can only change the `bar` attribute (and only for this request)

```bash
$ http PUT :8080/foo/25 bar=blip
HTTP/1.1 200 OK
content-length: 36
content-type: application/json
server: foo-service

{
    "foo": {
        "bar": "blip",
        "id": "25"
    }
}
```

### PATCH
Same as the PUT except uses a PATCH

### DELETE
Delete a foo. (Doesnt actually delete anything) Url is of pattern `/foo/:id`
where id is the fooid.

```bash
http DELETE :8080/foo/20
HTTP/1.1 204 No Content
content-length: 0
content-type: application/json
server: foo-service

```


