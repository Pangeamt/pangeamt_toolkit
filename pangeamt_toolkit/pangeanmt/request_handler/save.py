from aiohttp import web

async def save(req):
    nmt = req.app['nmt']
    new_model_dir = req.app['new_model_dir']
    lock = req.app['lock']
    ol = req.app['ol']

    try:
        if not ol:
            raise Exception('Online Learning is not active.')
        async with lock:
            nmt.save_model(new_model_dir)
        resp = {
            'rc': 0
        }
        return web.json_response(resp, status=200)

    except Exception as e:
        response_obj = {'status': 'failed', 'reason': str(e)}
        return web.json_response(response_obj, status=500)
