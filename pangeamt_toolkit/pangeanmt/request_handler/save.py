from aiohttp import web
import time

async def save(req):
    nmt = req.app['nmt']
    lock = req.app['lock']
    ol = req.app['ol']
    engine_path = req.app['engine_path']
    log = req.app['log_path']

    try:
        if not ol:
            raise Exception('Online Learning is not active.')
        async with lock:
            req = await req.json()
            while engine_path[-1] == '/':
                engine_path = engine_path[:-1]
            engine_folder = ('/').join(engine_path.split('/')[:-1])
            extend = '/extended_model'
            path = f"/{engine_folder}/{req['name']}{extend}"
            nmt.save_model(path)
            time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
            with open(log, 'a+') as file:
                words = ['new_name:']
                file.write(f'----Saving----\n'\
                    f'{time_string}\n'\
                    f'{words[0]:>17} {req["name"]}\n\n')
            resp = {
                'rc': 0
            }
            return web.json_response(resp, status=200)

    except Exception as e:
        response_obj = {'status': 'failed', 'reason': str(e)}
        with open(log, 'a+') as file:
            named_tuple = time.localtime()
            time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
            file.write(f'--Failed Save--\n'\
                f'{time_string}\n'\
                f'reason: {str(e)}\n\n')
        return web.json_response(response_obj, status=500)
