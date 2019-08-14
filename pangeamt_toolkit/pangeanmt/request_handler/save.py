from aiohttp import web

async def save(req):
    nmt = req.app['nmt']
    lock = req.app['lock']
    ol = req.app['ol']
    engine_path = req.app['engine_path']

    try:
        if not ol:
            raise Exception('Online Learning is not active.')
        async with lock:
            req = await req.json()
            while engine_path[-1] == '/':
                engine_path = engine_path[:-1]
            engine_folder = ('/').join(engine_path.split('/')[:-1])
            extend = '/extended_model'
            path = f"/{engine_folder}/{req['name']}{extend}"
            nmt.save_model(path)
            resp = {
                'rc': 0
            }
            return web.json_response(resp, status=200)

    except Exception as e:
        response_obj = {'status': 'failed', 'reason': str(e)}
        return web.json_response(response_obj, status=500)
