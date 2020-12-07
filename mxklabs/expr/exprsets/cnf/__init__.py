import json
import os

from .semantics import *

_exprdescrs_file = os.path.join(os.path.dirname(__file__), 'exprdescrs.json')

with open(_exprdescrs_file, 'r') as descrs:
  exprdescrs = json.loads(descrs.read())

