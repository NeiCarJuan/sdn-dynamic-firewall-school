# API Contract (Controller <-> Portal/Dashboard)

## POST /api/login
Body JSON:
{
  "mac": "...",
  "ip": "...",
  "username": "...",
  "role": "student|teacher|guest"
}

## GET /api/hosts
## GET /api/alerts
## GET /api/learned
(Optional) GET /api/rules
