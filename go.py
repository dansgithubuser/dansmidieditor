#!/usr/bin/env python

import os
import subprocess
import sys

sys.path.append(os.path.abspath('src'))

try: os.mkdir('built')
except: pass
os.chdir('built')
if '-r' not in sys.argv:
	subprocess.check_call('cmake -DCMAKE_BUILD_TYPE=Release ../deps/danssfml/wrapper'.split())
	subprocess.check_call('cmake --build . --config Release'.split())

from dansmidieditor import main
main()
