# URL Shortener Project Documentation

## Project Overview

**LinkNex** is a full-stack URL shortening service built with modern web technologies. It provides fast, secure, and scalable URL shortening capabilities with custom aliases, expiration dates, and comprehensive caching.

## Architecture

### Tech Stack

**Backend:**
- **FastAPI** - High-performance Python web framework
- **PostgreSQL** - Primary database for URL storage
- **Redis** - Caching layer for improved performance
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migration management
- **Pydantic** - Data validation and settings management

**Frontend:**
- **Next.js 16** - React framework with App Router
- **React 19** - UI library with latest features
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS 4** - Utility-first CSS framework
- **Axios** - HTTP client for API communication
- **React Hot Toast** - Toast notifications

## Project Structure

```
url-shortner/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/     # API endpoints
│   │   ├── core/                 # Configuration & health checks
│   │   ├── database/             # Database & Redis connections
│   │   ├── middleware/           # Rate limiting middleware
│   │   ├── models/               # SQLAlchemy models
│   │   ├── schemas/              # Pydantic schemas
│   │   ├── services/             # Business logic
│   │   └── utils/                # Utility functions
│   ├── alembic/                  # Database migrations
│   └── tutorial/                 # Documentation
├── frontend/
│   └── src/
│       ├── app/                  # Next.js App Router
│       ├── components/           # React components
│       ├── interfaces/           # TypeScript interfaces
│       └── services/             # API services
└── URL_Shortener_API.postman_collection.json
```

## Key Features Implemented

### 1. URL Shortening Algorithm
- **Entropy-based generation** using SHA-256 hashing
- **Base62 encoding** (a-z, A-Z, 0-9) for URL-safe codes
- **Collision detection** with automatic retry mechanism
- **Custom alias support** with validation

### 2. Database Design
```sql
CREATE TABLE urls (
    id UUID PRIMARY KEY,
    long_url VARCHAR UNIQUE NOT NULL,
    short_code VARCHAR UNIQUE NOT NULL,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 3. Caching Strategy
- **Multi-level caching**:
  - In-memory TTL cache (5 min) for hot URLs
  - Redis cache (24 hours) for persistent storage
  - Database as final fallback
- **Cache invalidation** on URL deletion
- **Pipeline operations** for atomic Redis operations

### 4. Rate Limiting
- **Endpoint-specific limits**:
  - URL creation: 10 requests/minute
  - Redirects: 1000 requests/minute
- **IP-based tracking** with sliding window
- **Async implementation** for better performance

### 5. Security Features
- **CORS configuration** with specific origins
- **Security headers**:
  - X-Content-Type-Options: nosniff
  - X-Frame-Options: DENY
  - X-XSS-Protection: 1; mode=block
- **Input validation** with Pydantic schemas
- **SQL injection prevention** via SQLAlchemy ORM

## API Endpoints

### Core Endpoints

#### Create Short URL
```http
POST /api/v1/urls/create
Content-Type: application/json

{
  "original_url": "https://example.com/very/long/url",
  "custom_alias": "my-link",
  "expires_in_days": 30
}
```

#### Redirect to Original URL
```http
GET /{short_code}
```

#### List URLs (Paginated)
```http
GET /api/v1/urls/list?page=1&limit=10
```

#### Delete URL
```http
DELETE /api/v1/urls/delete?short_code=abc123
```

### Health Check Endpoints
```http
GET /health          # Basic health check
GET /health/db       # Database health with metrics
```

## Implementation Details

### URL Generation Process
1. **Input validation** - Validate URL format and custom alias
2. **Duplicate check** - Check if URL already exists
3. **Code generation** - Generate unique short code using entropy-based algorithm
4. **Database storage** - Store with expiration date
5. **Cache population** - Store in Redis for fast access

### Error Handling
- **Custom exceptions** for business logic errors
- **Graceful degradation** when cache is unavailable
- **Detailed error responses** with appropriate HTTP status codes
- **Database rollback** on transaction failures

### Performance Optimizations
- **Connection pooling** (PostgreSQL: 10 connections, max overflow: 5)
- **Batch operations** for database queries
- **Gzip compression** for responses
- **Optimized queries** selecting only required fields
- **Pipeline operations** for Redis

## Frontend Implementation

### Component Architecture
- **UrlShortenerForm** - Main form component with validation
- **Responsive design** with mobile-first approach
- **Real-time validation** with visual feedback
- **Toast notifications** for user feedback

### State Management
- **React hooks** (useState, useTransition, useCallback)
- **Form validation** with URL format checking
- **Error handling** with field-specific highlighting
- **Optimistic updates** with loading states

### UI/UX Features
- **Glassmorphism design** with backdrop blur effects
- **Gradient backgrounds** and hover animations
- **Copy to clipboard** functionality
- **Responsive breakpoints** for all screen sizes
- **Accessibility** with proper ARIA labels

## Configuration

### Environment Variables
```bash
# Backend (.env)
DATABASE_URL=postgresql://user:pass@localhost:5432/url_shortener_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
BASE_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:3000
CACHE_TTL=86400
DEBUG=true
```

### Database Migrations
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

## Deployment Considerations

### Production Optimizations
- **Environment-based configuration** with Pydantic Settings
- **Logging configuration** with structured logging
- **Health checks** for container orchestration
- **Database connection pooling** for scalability
- **Redis clustering** for high availability

### Security Hardening
- **Disable debug endpoints** in production
- **Environment variable validation**
- **Rate limiting** to prevent abuse
- **Input sanitization** and validation

## Performance Metrics

### Caching Effectiveness
- **Cache hit ratio** tracking
- **Response time improvements** (5-10x faster for cached URLs)
- **Database load reduction**

### Scalability Features
- **Horizontal scaling** support with stateless design
- **Database indexing** on frequently queried fields
- **Connection pooling** for efficient resource usage

## Development Setup

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Dependencies

### Backend Dependencies
```
fastapi==0.124.2
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
pydantic-settings==2.1.0
alembic==1.13.1
psycopg2-binary==2.9.9
redis==7.1.0
hiredis==2.3.2
orjson==3.9.15
cachetools==5.3.2
```

### Frontend Dependencies
```json
{
  "dependencies": {
    "axios": "^1.13.2",
    "next": "16.0.10",
    "react": "19.2.1",
    "react-dom": "19.2.1",
    "react-hot-toast": "^2.6.0"
  },
  "devDependencies": {
    "@tailwindcss/postcss": "^4",
    "@types/axios": "^0.9.36",
    "@types/node": "^20",
    "@types/react": "^19",
    "@types/react-dom": "^19",
    "babel-plugin-react-compiler": "1.0.0",
    "eslint": "^9",
    "eslint-config-next": "16.0.8",
    "tailwindcss": "^4",
    "typescript": "^5"
  }
}
```

## Future Enhancements

### Planned Features
- **Analytics dashboard** with click tracking
- **Bulk URL creation** API
- **QR code generation** for short URLs
- **User authentication** and URL management
- **Custom domains** support
- **API rate limiting** with user tiers

### Technical Improvements
- **Monitoring and alerting** with Prometheus/Grafana
- **Load balancing** with multiple backend instances
- **CDN integration** for global performance
- **Database sharding** for massive scale

---

This documentation provides a comprehensive overview of the URL shortener implementation, covering architecture, features, and technical details for both development and production use.