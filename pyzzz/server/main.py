import sys
import os

cwd = os.getcwd()
sys.path.append(cwd)
print(f"cwd {cwd}")

reload = False
if len(sys.argv) >= 2 and sys.argv[1] == "reload":
    reload = True

import uvicorn
from pyzzz.server.app import app

uvicorn.run(app, port=5000, log_level="debug", reload=reload)
