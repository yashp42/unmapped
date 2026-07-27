# Unmapped — Music Culture Platform

A React frontend + FastAPI backend + MongoDB platform for exploring music culture, artists, albums, tracks, lore, theories, and connections.

## Quick Start (Local)

### Backend

```powershell
cd app/backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python -m uvicorn app.backend.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend

```powershell
cd app/frontend
npm install
REACT_APP_BACKEND_URL=http://127.0.0.1:8000 npm start
```

- Frontend: `http://localhost:3000`
- Backend API: `http://127.0.0.1:8000/api`

## Deploy with Docker

### Prerequisites

- Docker and Docker Compose installed

### Start the stack

```powershell
docker compose up --build
```

This starts:
- **Backend** at `http://localhost:8000`
- **Frontend** at `http://localhost:3000`
- **MongoDB** on port 27017 (internal only)

### First time setup

After the stack starts, seed the admin user:

```powershell
docker compose exec backend python -c "from seed import seed_database; import asyncio; asyncio.run(seed_database())"
```

Or run the reset script:

```powershell
C:\Users\YASH PATIL\Downloads\unmapped\app\backend\.venv\Scripts\python.exe scripts\reset_admin_password.py
```

### Environment variables

The app uses `app/backend/.env` for configuration. Key settings:

| Variable | Default | Description |
|---|---|---|
| `MONGO_URL` | `mongodb://mongo:27017` | MongoDB connection (use `mongodb://mongo:27017` in Docker) |
| `JWT_SECRET` | auto-generated (dev) | Strong secret for production |
| `CORS_ORIGINS` | `http://localhost:3000` | Comma-separated allowed origins |
| `PUBLIC_API_URL` | `http://127.0.0.1:8000` | Base URL for uploaded media |
| `ENVIRONMENT` | `development` | Set to `production` for production |
| `ADMIN_EMAIL` | `admin@unmapped.fm` | Admin seed email |
| `ADMIN_HANDLE` | `admin` | Admin seed handle |
| `ADMIN_PASSWORD` | `changeme` | Admin seed password |

## Project Structure

```
app/
  backend/       # FastAPI backend
    main.py      # App entry point
    server.py    # Alternative entry point (for ASGI servers)
    config.py    # Settings
    routes/      # API route handlers
    services/    # Business logic
    repositories/# Data access
    schemas/     # Pydantic models
    database/    # MongoDB connection + indexes
  frontend/      # React app (CRA + react-scripts)
scripts/         # Utility scripts
```
