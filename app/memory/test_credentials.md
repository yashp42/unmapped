"# Test Credentials — Unmapped (Music Culture Platform)

## Admin
- Email: `admin@unmapped.fm`
- Password: `unmapped2026`
- Role: `admin`

## Demo User (seeded)
- Email: `curator@unmapped.fm`
- Password: `curator2026`
- Role: `curator`

## Auth Endpoints (all under /api)
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/logout
- GET  /api/auth/me

Auth uses httpOnly cookies (access_token, refresh_token). Frontend uses `withCredentials: true`.
"