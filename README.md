# FastAPI Auth Module (PostgreSQL)

## What's included
- **signup** (email + password, role-aware: student / recruiter)
- **email verification** — token emailed, expires in 24h
- **login → JWT**
- **role-based middleware** (`require_role`) — protects routes by student/recruiter/admin
- **forgot / reset password** — same hashed-token pattern, expires in 1h
- **schema.sql** — standalone PostgreSQL DDL for `users`, `students`, `recruiters`, `recruiter_orgs`, `email_verifications`

## 1. Install PostgreSQL & create the database

If you don't have Postgres running locally:
- **Easiest for a hackathon:** use a free hosted instance — [Neon](https://neon.tech) or [Supabase](https://supabase.com) both give you a free Postgres + connection string in under a minute, no local install needed.
- **Local:** install Postgres, then:
  ```bash
  createdb placement_portal
  ```

## 2. Backend setup

```bash
cd portal-fastapi
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Fill in `.env`:
- **DATABASE_URL**: your Postgres connection string
- **JWT_SECRET**: any long random string (`python -c "import secrets; print(secrets.token_hex(32))"`)
- **SMTP_***: same Gmail App Password approach as before — Google Account → Security → App Passwords

Run it:
```bash
uvicorn app.main:app --reload
```
Server starts on `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs` — FastAPI gives you this for free, great for testing signup/login without a frontend yet.

Tables are auto-created on startup (`Base.metadata.create_all`) — fine for a hackathon. Swap to Alembic migrations once your schema stabilizes.

## 3. Schema notes

- `email_verifications` is reused for **both** email verification and password reset — the `purpose` column (`verify_email` / `reset_password`) distinguishes them, so you don't need two near-identical tables.
- Only the **hash** of each token is stored (SHA-256) — the raw token exists only in the emailed link, so a database leak alone can't be used to verify accounts or reset passwords.
- `recruiter_orgs` auto-creates an org row from the signup email's domain if one doesn't exist yet (e.g. first person from `dabur.com` creates the "Dabur" org). For production you'd likely require orgs to be pre-approved instead of auto-created — flag this as a known simplification if judges ask.
- `students` and `recruiters` are separate tables linked 1:1 to `users` (rather than one giant `users` table with nullable columns) — keeps each role's fields clean and makes the schema easy to extend per role later (e.g. adding `verification_status` fields only to `students`).

## 4. Role-based middleware — how to use it

```python
from app.api.deps import require_role
from app.models.models import UserRole

@router.get("/candidates/search")
def search_candidates(current_user: User = Depends(require_role(UserRole.recruiter, UserRole.admin))):
    ...
```

Any route that just needs "someone logged in, any role" uses `Depends(get_current_user)` instead. Both are in `app/api/deps.py`, and `app/api/routes/examples.py` has three working examples you can hit directly to test role gating.

## 5. Quick test flow (via /docs)

1. `POST /api/auth/signup` with a student — check your inbox for the verification email
2. Click the link → hits `GET /api/auth/verify-email/{token}` automatically if your frontend route exists, or just copy the token from the link and call it directly in `/docs`
3. `POST /api/auth/login` → copy the `access_token`
4. Click "Authorize" in `/docs`, paste the token, then try `GET /api/me` and `GET /api/recruiter-only` (should 403 for a student) to see the role gate working

## 6. Next steps
- Add `alembic init alembic` once you want real migrations instead of `create_all`
- Add rate limiting on `/login` and `/forgot-password` before this goes near production
- This is a separate stack from the earlier Node/Express + MongoDB version — pick one for your actual SIH build; don't run both in the final submission
