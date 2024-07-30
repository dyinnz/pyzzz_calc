import os
import sys

filepath = os.path.realpath(__file__)
project = os.path.dirname(os.path.dirname(filepath))
sys.path.insert(0, project)

import pyzzz
