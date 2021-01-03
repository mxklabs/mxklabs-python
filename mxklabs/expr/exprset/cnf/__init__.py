import json
import os

from .semantics import *

_definition_file = os.path.join(os.path.dirname(__file__), 'definition.json')

with open(_definition_file, 'r') as deffile:
  definition = json.loads(deffile.read())

