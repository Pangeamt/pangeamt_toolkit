import time
from aiohttp import web as _web
from pangeamt_toolkit import Seg

async def translate(req):
    nmt = req.app['nmt']
    pipeline = req.app['pipeline']
    lock = req.app['lock']
    sem = req.app['sem']
    log = req.app['trans_log']

    try:
        req = await req.json()
        batch_to_trans = []
        segs = []
        async with sem:
            for tu in req.get('tus'):
                seg = Seg(tu['src'])
                pipeline.preprocess(seg)
                batch_to_trans.append(seg.src)
                segs.append(seg)

        async with lock:
            translations = nmt.translate(batch_to_trans)

        for tu in req.get('tus'):
            named_tuple = time.localtime() # get struct_time
            time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
            seg = segs.pop(0)
            translation = translations.pop(0)
            seg.tgt = seg.tgt_raw = (' ').join(translation.tgt)
            pipeline.postprocess(seg)
            with open(log, 'a+') as file:
                words = ['source:', 'source_prep:', 'translation:',
                    'translation_post:', 'score:']
                file.write(f'{time_string}\n'\
                    f'{words[0]:>17} {seg.src_raw}\n'\
                    f'{words[1]:>17} {seg.src}\n'\
                    f'{words[2]:>17} {seg.tgt_raw}\n'\
                    f'{words[3]:>17} {seg.tgt}\n'\
                    f'{words[4]:>17} {translation.pred_score}\n\n')
            tu['tgt'] = seg.tgt

        return _web.json_response(req, status=200)

    except Exception as e:
        response_obj = {'status': 'failed', 'reason': str(e)}
        return _web.json_response(response_obj, status=500)
