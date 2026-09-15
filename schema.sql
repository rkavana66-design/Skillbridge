-- Placement Portal — PostgreSQL Schema
-- Run this directly with: psql -d placement_portal -f schema.sql
-- (Or let Alembic generate/manage it from the SQLAlchemy models instead — see README)

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TYPE user_role AS ENUM ('student', 'recruiter', 'admin');

-- ---------- users ----------
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email           VARCHAR(255) UNIQUE NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    role            user_role NOT NULL DEFAULT 'student',
    is_verified     BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_users_email ON users(email);

-- ---------- students ----------
CREATE TABLE students (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name            VARCHAR(255) NOT NULL,
    discipline      VARCHAR(100),        -- e.g. IT, Medical, Healthcare-Tech
    github_url      VARCHAR(255),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------- recruiter_orgs ----------
CREATE TABLE recruiter_orgs (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name            VARCHAR(255) NOT NULL,
    domain          VARCHAR(255) UNIQUE NOT NULL,   -- e.g. dabur.com — used to auto-verify recruiter signups
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_recruiter_orgs_domain ON recruiter_orgs(domain);

-- ---------- recruiters ----------
CREATE TABLE recruiters (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    org_id          UUID REFERENCES recruiter_orgs(id) ON DELETE SET NULL,
    name            VARCHAR(255) NOT NULL,
    designation     VARCHAR(150),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------- email_verifications ----------
-- Reused for both email verification and password reset tokens (see `purpose`)
CREATE TABLE email_verifications (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash      VARCHAR(64) NOT NULL,   -- SHA-256 hash of the raw token (raw token only ever goes in the email)
    purpose         VARCHAR(30) NOT NULL DEFAULT 'verify_email',  -- 'verify_email' | 'reset_password'
    expires_at      TIMESTAMPTZ NOT NULL,
    used_at         TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_email_verifications_token_hash ON email_verifications(token_hash);
CREATE INDEX idx_email_verifications_user_id ON email_verifications(user_id);
