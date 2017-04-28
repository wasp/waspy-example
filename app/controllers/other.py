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
    body = request.json()
    service = body.get('service')
    path = body.get('path')
    data = body.get('body')
    method = body.get('method')

    if path is None:
        raise ResponseError('No path provided', 400,
                            reason="'path' is a required field.")
    app: Application = request.app
    response = await app.client.make_request(method, service, path, data,
                                             context=request)
    return {
        'result':
            {'status_code': response.status,
             'body': response.body,
             'headers': response.headers,
             }
    }


async def ping(request):
    return {'result': 'pong '}
