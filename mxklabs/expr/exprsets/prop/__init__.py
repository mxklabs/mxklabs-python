import json
import os

_exprdefs_file = os.path.join(os.path.dirname(__file__), 'exprdefs.json')

with open(_exprdefs_file, 'r') as defs:
  exprdefs = json.loads(defs.read())