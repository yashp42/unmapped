# Unmapped — Music Culture Platform (MVP)

This repository contains a React frontend and a FastAPI backend backed by MongoDB (Motor).

## Local development

### Backend setup

1. Create a Python virtual environment and install dependencies:

```powershell
cd app/backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

2. Copy `.env.example` to `app/backend/.env` and update values:

```powershell
copy .env.example .env
```

3. If you have a local MongoDB server, use:

```powershell
MONGO_URL=mongodb://localhost:27017
```

If you use Atlas, set your cluster string instead.

4. Run the backend:

```powershell
cd ..\..
& "c:/Users/YASH PATIL/Downloads/unmapped/app/backend/.venv/Scripts/python.exe" -m uvicorn app.backend.main:app --reload --host 127.0.0.1 --port 8000
```

The API root is at `http://127.0.0.1:8000`, with endpoints under `/api`.

### Frontend setup

1. Install frontend dependencies:

```bash
cd app/frontend
npm install
```

2. Start the frontend development server:

```bash
REACT_APP_BACKEND_URL=http://127.0.0.1:8000 npm start
```

3. Open the site in the browser at `http://localhost:3000`.

## MongoDB flow and diagnostics

### Running the integration diagnostic scripts

From repo root, run:

```powershell
& "c:/Users/YASH PATIL/Downloads/unmapped/app/backend/.venv/Scripts/python.exe" scripts/atlas_network_test.py
& "c:/Users/YASH PATIL/Downloads/unmapped/app/backend/.venv/Scripts/python.exe" scripts/mongo_crud_test.py
```

- `atlas_network_test.py` checks DNS, TCP, and SSL/TLS handshake behavior against the Atlas shard hosts.
- `mongo_crud_test.py` runs a simple insert/read/update/delete cycle against the configured `MONGO_URL`.

### Local Mongo fallback

If Atlas is not reachable, use a local Mongo server and update `app/backend/.env`:

```text
MONGO_URL=mongodb://localhost:27017
```

Then rerun the backend.

## GitHub push instructions

1. Initialize repo if needed:

```powershell
git init
```

2. Add files and commit:

```powershell
git add .
git commit -m "Initial MVP backend/frontend integration"
```

3. Add remote and push:

```powershell
git branch -M main
git remote add origin https://github.com/<your-org>/<your-repo>.git
git push -u origin main
```

## Notes

- Backend code is under `app/backend`.
- Frontend code is under `app/frontend`.
- JWT auth is implemented in the backend; login returns `access_token`.
- Collection edit/delete flows have modal and loading UI.

## Next steps

- Fix Mongo Atlas TLS connectivity or run against a local Mongo instance.
- Add complete CRUD test coverage for all routes.
- Continue modularizing backend services and adding validations.
