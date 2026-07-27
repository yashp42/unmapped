import importlib
import sys
try:
    import os
    print('cwd=', os.getcwd())
    print('sys.path[0]=', sys.path[0])
    print('listing root:', os.listdir('.'))
    # ensure project root is on sys.path so 'app' can be imported
    sys.path.insert(0, os.getcwd())
    importlib.import_module('app.backend.routes.albums')
    print('import ok')
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)
