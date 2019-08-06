from aiohttp import web

async def train(req):
    nmt = req['nmt']
    pipeline = req['pipeline']
    lock = req['lock']
    try:
        req = await req.json() # TODO sensitive point
        async with lock:
            for tu in req['tus']:
                src_preprocessed = pipeline.preprocess(tu['src'])
                tgt_preprocessed = pipeline.preprocess(tu['tgt'])

                nmt.train(src_preprocessed, tgt_preprocessed)
        resp = {
            'rc': 0
        }
        return web.json_response(resp, status=200)

    except Exception as e:
        response_obj = {'status': 'failed', 'reason': str(e)}
        return web.json_response(response_obj, status=500)
