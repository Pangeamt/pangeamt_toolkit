import time
from aiohttp import web as _web
from pangeamt_toolkit import Seg

async def translate(req):
    nmt = req.app['nmt']
    pipeline = req.app['pipeline']
    lock = req.app['lock']
    sem = req.app['sem']
    log = req.app['log_path']

    try:
        req = await req.json()
        batch_to_trans = []
        segs = []
        async with sem:
            for src in req.get('srcs'):
                seg = Seg(src)
                pipeline.preprocess(seg)
                batch_to_trans.append(seg.src)
                segs.append(seg)

        async with lock:
            translations = nmt.translate(batch_to_trans)

        ans = {
            'tus':[]
        }

        for _ in range(len(req.get('srcs'))):
            named_tuple = time.localtime() # get struct_time
            time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
            seg = segs.pop(0)
            translation = translations.pop(0)
            seg.tgt = seg.tgt_raw = (' ').join(translation.tgt)
            pipeline.postprocess(seg)
            with open(log, 'a+') as file:
                words = ['source:', 'source_prep:', 'translation:',
                    'translation_post:', 'score:']
                file.write(f'----Translating----\n'\
                    f'{time_string}\n'\
                    f'{words[0]:>17} {seg.src_raw}\n'\
                    f'{words[1]:>17} {seg.src}\n'\
                    f'{words[2]:>17} {seg.tgt_raw}\n'\
                    f'{words[3]:>17} {seg.tgt}\n'\
                    f'{words[4]:>17} {translation.pred_score}\n\n')
            ans['tus'].append({'src': seg.src, 'tgt': seg.tgt})

        return _web.json_response(ans, status=200)

    except Exception as e:
        response_obj = {'status': 'failed', 'reason': str(e)}
        with open(log, 'a+') as file:
            named_tuple = time.localtime()
            time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
            file.write(f'--Failed Translation--\n'\
                f'{time_string}\n'\
                f'reason: {str(e)}\n\n')
        return _web.json_response(response_obj, status=500)
