import json
import random
import string

from waspy import Request, ResponseError, Application


async def error(request: Request):
    error_code = request.query.get('error_code', '400')
    try:
        error_code = int(error_code)
    except ValueError:
        # The following will skip middlewares on the way out
        raise ResponseError('Not a valid error code', 400,
                            reason="'error_code' parameter "
                                   "must be an integer.")
    # the following will NOT skip middlewares on the way out
    return {'code': error_code, 'message': 'here is a message'}, error_code


async def callback(request: Request):
    try:
        body = request.json()
    except json.JSONDecodeError:
        raise ResponseError('Invalid json', 400, reason='Invalid json')

    service = body.get('service')
    port = body.get('port')
    path = body.get('path')
    data = body.get('body')
    method = body.get('method')

    if method is None:
        raise ResponseError('No method provided', 400,
                            reason="'method' is a required field")

    if path is None:
        raise ResponseError('No path provided', 400,
                            reason="'path' is a required field.")
    app: Application = request.app
    response = await app.client.make_request(method, service, path, data,
                                             context=request, port=port)

    try:
        body = response.json()
    except json.JSONDecodeError:
        body = response.body.decode()

    return {
        'result':
            {'status_code': response.status,
             'body': body,
             'headers': response.headers,
             }
    }

async def ping(request):
    return {'result': 'pong'}


async def large(request):
    # this currently produces ~ 9.6MB of text/json
    main = ''.join(random.choice(string.ascii_letters + string.digits)
                   for _ in range(1000))
    final = ''.join(main for _ in range(10000))
    return {'something_large': final}
