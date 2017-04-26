#!/usr/bin/env python3

import sys
import app
from os.path import abspath
from os.path import dirname


sys.path.insert(0, abspath(dirname(__file__)))
application = app.app
