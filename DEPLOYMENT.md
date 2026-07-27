# Deployment checklist

1. Set `ENVIRONMENT=production`, a unique `JWT_SECRET`, production `MONGO_URL`, and exact `CORS_ORIGINS` in `app/backend/.env`. Do not commit this file.
2. Build and run locally with `docker compose up --build`.
3. Verify `http://localhost:8001/api/health`, sign in, publish a test item, then delete it through the admin CMS.
4. Enable managed Mongo backups and alerting before public launch. Keep API and Mongo private; expose only the frontend and API through HTTPS.
5. Configure an uptime check against `/api/health` and inspect structured server logs for provider failures and `429` publishing responses.

The included GitHub Actions workflow compiles the backend and produces a production frontend build on every push and pull request.
