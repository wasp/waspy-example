from copy import copy

from waspy import Response, JSONDecodeError, QueryParams


async def echo_request(request):
    response = {
        'headers': copy(request.headers),
        'query_string': request.query_string,
        'query': request.query.mappings,
        'url': request.path,
    }
    return response


async def echo_body(request):
    try:
        return request.json()
    except JSONDecodeError:
        return Response(body=request.body, content_type=request.content_type)
