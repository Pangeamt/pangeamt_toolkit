import os
import sys
import json
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

current_dir = os.path.abspath(os.path.dirname(__file__))
os.chdir(current_dir)

class PangeanmtServer:
    def __init__(self, model_path):
        self._app = web.Application()
        extended_model_path = model_path + "/extended_model"
        config_path = extended_model_path + '/config.json'
        with open(config_path, 'r') as file:
            config = json.loads(file.read())

        self._app['nmt'] = Pangeanmt(extended_model_path) # config['model'] ?
        self._app['pipeline'] = Pipeline(config['pipeline_config'])
        self._app['pipeline_tgt'] = Pipeline(config['pipeline_config_tgt'])
        self._app['model_path'] = model_path
        self._app['lock'] = asyncio.Lock()
        self._app['sem'] = asyncio.Semaphore()
        self._app['ol'] = config['online_learning']['active']

        self._app.router.add_post('/save', save)
        self._app.router.add_post('/train', train)
        self._app.router.add_post('/isready', ready)
        self._app.router.add_post('/translate', translate)

    def start(self):
        web.run_app(self._app, port=8081)
