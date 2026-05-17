from pathlib import Path
import sys

# Ensure package imports work when running from the `app/backend` folder
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.main import app  # expose FastAPI app for ASGI servers
