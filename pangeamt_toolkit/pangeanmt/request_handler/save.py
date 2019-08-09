from aiohttp import web

async def save(req):
    nmt = req.app['nmt']
    lock = req.app['lock']
    ol = req.app['ol']
    model_path = req.app['model_path']

    try:
        if not ol:
            raise Exception('Online Learning is not active.')
        async with lock:
            req = await req.json()
            list_path = model_path.split('/')
            if list_path[-1] == '':
                main_path = ('/').join(list_path[:-2])
            else:
                main_path = ('/').join(list_path[:-1])
            extend = '/extended_model'
            path = main_path + f"/{list_path[-2]}_{req['name']}{extend}"
            nmt.save_model(path)
            resp = {
                'rc': 0
            }
            return web.json_response(resp, status=200)

    except Exception as e:
        response_obj = {'status': 'failed', 'reason': str(e)}
        return web.json_response(response_obj, status=500)
