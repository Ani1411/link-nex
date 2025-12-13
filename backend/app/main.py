import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import RedirectResponse, ORJSONResponse
from sqlalchemy.orm import Session
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.health import startup_health_check, get_database_health
from app.services.url_service import URLService
from app.database.database import get_db
from app.middleware.rate_limit import rate_limit_middleware
from cachetools import TTLCache

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# In-memory cache for hot URLs
url_cache = TTLCache(maxsize=10000, ttl=300)  # 5 min TTL

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    startup_health_check()
    yield
    pass

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="URL Shortener API",
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.CORS_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)
app.middleware("http")(rate_limit_middleware)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "URL Shortener API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/health/db")
async def db_health_check():
    """Comprehensive database health check with detailed metrics"""
    return get_database_health()


@app.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    """Redirect to the original URL given a short code"""
    
    # Check in-memory cache first
    if short_code in url_cache:
        return RedirectResponse(url=url_cache[short_code], status_code=status.HTTP_301_MOVED_PERMANENTLY)
    
    url = URLService.get_url_by_short_code(short_code=short_code, db=db)
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found")
    
    # Cache the result
    url_cache[short_code] = url.long_url
    
    return RedirectResponse(url=url.long_url, status_code=status.HTTP_301_MOVED_PERMANENTLY)