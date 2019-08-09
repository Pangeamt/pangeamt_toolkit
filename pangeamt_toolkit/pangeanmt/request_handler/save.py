from aiohttp import web

async def save(req):
    nmt = req.app['nmt']
    lock = req.app['lock']
    ol = req.app['ol']
    extended_path = req.app['extended_model_path']

    try:
        if not ol:
            raise Exception('Online Learning is not active.')
        async with lock:
            req = await req.json()
            path = ('/').join(extended_path.split('/')[:-1]) + f"_{req['name']}"
            nmt.save_model(path)
            resp = {
                'rc': 0
            }
            return web.json_response(resp, status=200)

    except Exception as e:
        response_obj = {'status': 'failed', 'reason': str(e)}
        return web.json_response(response_obj, status=500)
