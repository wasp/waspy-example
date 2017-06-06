

async def foo_get(request):
    foo_id = request.path_params.get('id')
    return {'foo': {'bar': 'baz', 'id': int(foo_id)}}


async def foo_put(request):
    foo_id = request.path_params.get('id')
    if foo_id != '25':
        return {'message': 'foo with id {} not found.'.format(foo_id)}, 404

    body = request.json()
    baz = body.get('bar', 'baz')
    return {'foo': {'bar': baz, 'id': '25'}}


async def foo_post(request):
    foo = request.json()
    foo['id'] = 25
    return {'foo': foo}, 201


async def foo_patch(request):
    foo_id = request.path_params.get('id')
    body = request.json()
    baz = body.get('bar', 'baz')
    return {'foo': {'bar': baz, 'id': '25'}}


async def foo_delete(request):
    return None, 204