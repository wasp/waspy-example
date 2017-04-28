

async def attach_object(app, handler):
    """ This middleware shows an example of adding something
    to the request object """
    async def middleware(request):
        request.some_object = object()
        return await handler(request)
    return middleware


async def add_header(app, handler):
    """ This middleware inspects a response and adds some headers
    after the handler responds, but before it goes across the wire"""
    async def middleware(request):
        response = await handler(request)
        if response.headers.get('content-type') == 'application/json':
            response.headers['x_is_json'] = 'true'
        return response

    return middleware