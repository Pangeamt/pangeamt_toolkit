from aiohttp import web

async def train(req):
    nmt = req.app['nmt']
    pipeline = req.app['pipeline']
    pipeline_tgt = req.app['pipeline_tgt']
    lock = req.app['lock']
    ol = req.app['ol']

    try:
        if not ol:
            raise Exception('Online Learning is not active.')
        req = await req.json() # TODO sensitive point
        async with lock:
            for tu in req['tus']:
                src_preprocessed = pipeline.preprocess_str(tu['src'])
                print(src_preprocessed)
                tgt_preprocessed = pipeline_tgt.preprocess_str(tu['tgt'])
                print(tgt_preprocessed)

                nmt.train(src_preprocessed, tgt_preprocessed)
        resp = {
            'rc': 0
        }
        return web.json_response(resp, status=200)

    except Exception as e:
        response_obj = {'status': 'failed', 'reason': str(e)}
        return web.json_response(response_obj, status=500)
