from aiohttp import web
import time

async def save(req):
    nmt = req.app['nmt']
    lock = req.app['lock']
    ol = req.app['ol']
    model_path = req.app['model_path']
    log = req.app['log_path']

    try:
        if not ol:
            raise Exception('Online Learning is not active.')
        async with lock:
            path = os.path.join(model_path, "/translation_model_tmp")
            nmt.save_model(path)
            named_tuple = time.localtime()
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
