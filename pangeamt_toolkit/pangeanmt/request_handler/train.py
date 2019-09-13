from aiohttp import web
import time

async def train(req):
    nmt = req.app['nmt']
    pipeline = req.app['pipeline']
    pipeline_tgt = req.app['pipeline_tgt']
    lock = req.app['lock']
    ol = req.app['ol']
    log = req.app['log_path']

    try:
        if not ol:
            raise Exception('Online Learning is not active.')
        req = await req.json() # TODO sensitive point
        async with lock:
            for tu in req['tus']:
                if tu['tgt'] == '':
                    raise Exception('Missing target segment for Online '\
                        'Learning Training.')
                src_preprocessed = pipeline.preprocess_str(tu['src'])
                tgt_preprocessed = pipeline_tgt.preprocess_str(tu['tgt'])
                named_tuple = time.localtime() # get struct_time
                time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
                with open(log, 'a+') as file:
                    words = ['source:', 'source_prep:', 'target:',
                        'target_prep:', 'score:']
                    file.write(f'----Training----\n'\
                        f'{time_string}\n'\
                        f'{words[0]:>13} {tu["src"]}\n'\
                        f'{words[1]:>13} {src_preprocessed}\n'\
                        f'{words[2]:>13} {tu["tgt"]}\n'\
                        f'{words[3]:>13} {tgt_preprocessed}\n\n')
                nmt.train(src_preprocessed, tgt_preprocessed)
        resp = {
            'rc': 0
        }
        return web.json_response(resp, status=200)

    except Exception as e:
        response_obj = {'status': 'failed', 'reason': str(e)}
        with open(log, 'a+') as file:
            named_tuple = time.localtime()
            time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
            file.write(f'--Failed Train--\n'\
                f'{time_string}\n'\
                f'reason: {str(e)}\n\n')
        return web.json_response(response_obj, status=500)
