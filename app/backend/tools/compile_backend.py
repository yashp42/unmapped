import py_compile
import glob
import sys

files = glob.glob('**/*.py', recursive=True)
errs = 0
for f in files:
    try:
        py_compile.compile(f, doraise=True)
    except Exception as e:
        print('ERROR', f, e)
        errs += 1

if errs:
    print('COMPILE ERRORS:', errs)
    sys.exit(1)
print('OK', len(files), 'files compiled')
