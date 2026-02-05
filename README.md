# Giffy: Gift Chaos to Your Friends

Agentic, Microsoft-inspired multi-agent system that finds, curates, and chaotically suggests gifts for your friends. Bla bla.

## Monorepo Layout

- agent/ — agent runners and LLM provider wrappers
- server/ — FastAPI backend (auth, friends, gifts, social integrations)
- client/ — Next.js app (UI)

## Quick Start

Prerequisites:
- Python 3.10+
- Node.js 18+ and npm (or pnpm/yarn)
- PostgreSQL 14+ (local or Docker)

### 1) Environment Variables

Copy the example env files and fill in values.

- Agent
  - cp agent/.env.example agent/.env
- Server
  - cp server/.env.example server/.env

The backend reads DATABASE_URL from server/.env (default in code):
- DATABASE_URL=postgresql://postgres:password@localhost:5432/giftify
Adjust user/password/host/port/db to your local setup.

### 2) PostgreSQL Setup

Pick one of the options below to run Postgres locally.

- Local install (Linux/macOS/Homebrew/apt)
  - Create DB/user (example):
    - psql -U postgres -c "CREATE DATABASE giftify;"
    - psql -U postgres -c "ALTER USER postgres WITH PASSWORD 'password';"  # or create a dedicated user
  - Verify connection with psql or a GUI (ensure it matches DATABASE_URL).

- Docker (recommended for quick start)
  - docker run --name giftify-postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=giftify -p 5432:5432 -d postgres:15
  - Wait for container to be healthy, then ensure server/.env has the matching DATABASE_URL.

### 3) Backend (server)

Install Python dependencies and run the API.

- Create and activate a virtualenv (recommended)
  - python -m venv .venv
  - source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
- Install requirements
  - pip install -r server/requirements.txt
- Run database migrations/metadata (if applicable)
  - First run will auto-create tables via SQLAlchemy models if not present.
- Run the API (development)
  - uvicorn server.main:app --reload

API docs once running:
- http://localhost:8000/docs
- http://localhost:8000/redoc

### 4) Frontend (client)

Install dependencies and start the dev server.

- cd client
- npm i
- npm run dev

The app will be available at:
- http://localhost:3000

## Scripts (convenience)

- Backend: uvicorn server.main:app --reload
- Frontend: cd client && npm run dev
