#!/usr/bin/env python

import sys
from pangeamt_toolkit import PangeanmtServer

if len(sys.argv) < 2 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
    print('Syntax: pangeamt_build_server.py <path extended model>')

print(f'Loading {sys.argv[1]} model...')
server = PangeanmtServer(sys.argv[1])

server.start()
print('Server started')
