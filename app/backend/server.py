import sys
from pathlib import Path

# Ensure package imports work from either the repo root or `app/backend`.
BACKEND_ROOT = Path(__file__).resolve().parent
APP_ROOT = BACKEND_ROOT.parent
for path in (APP_ROOT, BACKEND_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from backend.main import app  # expose FastAPI app for ASGI servers
