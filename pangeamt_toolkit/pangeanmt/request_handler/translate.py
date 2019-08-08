from aiohttp import web as _web

async def translate(req):
    nmt = req.app['nmt']
    pipeline = req.app['pipeline']
    lock = req.app['lock']
    sem = req.app['sem']

    req = await req.json() # TODO sensitive point
    batch_to_trans = []
    async with sem:
        for tu in req.get('tus'):
            src_preprocessed = pipeline.preprocess_str(tu['src'])
            batch_to_trans.append(src_preprocessed)

    async with lock:
        translations = nmt.translate(batch_to_trans)

    for tu in req.get('tus'):
        translation = translations.pop(0)
        translation = (' ').join(translation.tgt)
        tu['tgt'] = pipeline.postprocess_str(translation)

    return _web.json_response(req, status=200)

#    except Exception as e:
#        response_obj = {'status': 'failed', 'reason': str(e)}
#        return _web.json_response(response_obj, status=500)
