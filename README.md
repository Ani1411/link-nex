# LinkNex - URL Shortener

A fast, secure URL shortening service built with FastAPI and Next.js.

## Features

- Shorten long URLs with custom aliases
- Set expiration dates for URLs
- Multi-level caching (Redis + in-memory)
- Rate limiting and security headers
- Responsive web interface
- URL management with pagination

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- PostgreSQL
- Redis

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your database credentials
alembic upgrade head
uvicorn app.main:app --reload
```

Backend runs on `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:3000`

## API Usage

### Create Short URL
```bash
curl -X POST "http://localhost:8000/api/v1/urls/create" \
  -H "Content-Type: application/json" \
  -d '{
    "original_url": "https://example.com/very/long/url",
    "custom_alias": "my-link",
    "expires_in_days": 30
  }'
```

### Access Short URL
```bash
curl "http://localhost:8000/abc123"
# Redirects to original URL
```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:pass@localhost:5432/url_shortener_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
BASE_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:3000
```

## Tech Stack

**Backend:** FastAPI, PostgreSQL, Redis, SQLAlchemy  
**Frontend:** Next.js 16, React 19, TypeScript, Tailwind CSS