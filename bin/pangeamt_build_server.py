#!/usr/bin/env python

import sys
from pangeamt_toolkit import PangeanmtServer

if len(sys.argv) < 2 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
    print('Syntax: pangeamt_build_server.py <path extended model>'\
        ' <path to save ol model (optional)>')
try:
    server = PangeanmtServer(sys.argv[1], sys.argv[2])
except:
    server = PangeanmtServer(sys.argv[1])

server.start()
