import os
import sys
import json
import time
import uvloop
import asyncio
from aiohttp import web
from pangeamt_toolkit.pangeanmt.request_handler.save import save
from pangeamt_toolkit.pangeanmt.request_handler.train import train
from pangeamt_toolkit.pangeanmt.request_handler.ready import ready
from pangeamt_toolkit.pangeanmt.request_handler.translate import translate
from pangeamt_toolkit import Pipeline
from pangeamt_toolkit.pangeanmt import Pangeanmt

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

class PangeanmtServer:
    def __init__(self, model_path):
        os.chdir(model_path)
        self._app = web.Application()
        config_path = os.path.join(model_path, "config.json")
        log_path = self._set_up_log(model_path)

        with open(log_path, 'a+') as file:
            named_tuple = time.localtime()
            time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
            file.write(f'--Starting Server--\n'\
                f'{time_string}\n\n')

        with open(config_path, 'r') as file:
            config = json.loads(file.read())

        self._app['nmt'] = Pangeanmt(model_path)

        self._app['pipeline'] = Pipeline(config['pipeline_config'],\
            config['src_lang'], config['tgt_lang'])

        self._app['pipeline_tgt'] = Pipeline(config['pipeline_config_tgt'],\
            config['tgt_lang'])

        self._app['model_path'] = model_path
        self._app['lock'] = asyncio.Lock()
        self._app['sem'] = asyncio.Semaphore()
        self._app['ol'] = config['online_learning']['active']
        self._app['log_path'] = log_path

        self._app.router.add_post('/save', save)
        self._app.router.add_post('/train', train)
        self._app.router.add_post('/isready', ready)
        self._app.router.add_post('/translate', translate)

    def start(self):
        web.run_app(self._app, port=8081)

    def _set_up_log(self, model_path):
        while model_path[-1] == '/':
            model_path = model_path[:-1]
        model_name = model_path.split('/')[-1]
        log_name = f'log_{model_name}.txt'
        logs_dir = f'{("/").join(model_path.split("/")[:-1])}/logs/'
        print(logs_dir)
        try:
            os.mkdir(logs_dir)
        except:
            pass
        return f'{logs_dir}/{log_name}'
