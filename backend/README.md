# URL Shortener Backend

FastAPI-based URL shortening service with PostgreSQL and Redis.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Configure your .env file
alembic upgrade head
uvicorn app.main:app --reload
```

## Environment Variables

```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/url_shortener_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
BASE_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:3000
CACHE_TTL=86400
DEBUG=true
```

## API Endpoints

- `POST /api/v1/urls/create` - Create short URL
- `GET /{short_code}` - Redirect to original URL
- `GET /api/v1/urls/list` - List URLs (paginated)
- `DELETE /api/v1/urls/delete` - Delete URL
- `GET /health` - Health check

## Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

## Development

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```