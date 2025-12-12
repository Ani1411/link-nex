from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.config import settings

from fastapi import Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.services.url_service import URLService
from app.database.database import get_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="URL Shortener API"
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "URL Shortener API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/{short_code}")
async def redirect_url(short_code:str, db: Session = Depends(get_db)):
    """Redirect to the original URL given a short code"""

    url = URLService.get_url_by_short_code(short_code=short_code, db=db)
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found")
    
    return RedirectResponse(url=url.long_url, status_code=status.HTTP_301_MOVED_PERMANENTLY)