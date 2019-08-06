import os
import sys
import json
import uvloop
import asyncio
from aiohttp import web
from pangeamt_toolkit.pangeanmt.request_handler.save import save
from pangeamt_toolkit.pangeanmt.request_handler.train import train
from pangeamt_toolkit.pangeanmt.request_handler.translate import translate
from pangeamt_toolkit.pangeanmt import Pangeanmt

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

current_dir = os.path.abspath(os.path.dirname(__file__))
os.chdir(current_dir)

class PangeanmtServer:
    def __init__(self, extended_model_path, new_model_path):
        app = web.Application()
        config_path = extended_model_path + '/config.json'
        with open(config_path, 'r') as file:
            config = json.loads(file.read())

        app['nmt'] = Pangeanmt(extended_model_path) # Can use config['model']
        app['new_model_path'] = new_model_path
        app['pipeline'] = Pipeline(config['pipeline_config'])
        app['lock'] = asyncio.Lock()

        app.router.add_post('/save', save)
        app.router.add_post('/train', train)
        app.router.add_post('/translate', translate)

    def start(self):
        web.run_app(app, port=8081)
