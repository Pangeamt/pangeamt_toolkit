from aiohttp import web

async def translate(req):
    nmt = req['nmt']
    pipeline = req['pipeline']
    lock = req['lock']
    
    try:
        req = await req.json() # TODO sensitive point
        async with lock:
            for tu in req.get('tus'):
                src_preprocessed = pipeline.preprocess(tu['src'])
                batch_to_trans.append(src_preprocessed)

            translations = nmt.translate(batch_to_trans)

            for tu in req.get('tus'):
                tu['tgt'] = pipeline.postprocess(translations.pop(0))

        return web.json_response(req, status=200)

    except Exception as e:
        response_obj = {'status': 'failed', 'reason': str(e)}
        return web.json_response(response_obj, status=500)
