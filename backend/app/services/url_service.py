from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta, timezone
from app.utils.url_generator import generate_entropy_code


class URLAlreadyExistsError(Exception):
    def __init__(self, existing_url):
        self.existing_url = existing_url
        super().__init__("URL already exists")


class ShortCodeAlreadyExistsError(Exception):
    pass


class URLService:
    
    @staticmethod
    def create_short_url(db: Session, original_url: str, short_code: str = None, expires_in_days=30):
        from app.models.url import URL
        
        # Check if URL already exists when custom alias is provided
        if short_code:
            existing_url = db.query(URL).filter(URL.long_url == original_url).first()
            if existing_url:
                raise URLAlreadyExistsError(existing_url)
        
        # Generate short code if not provided
        if not short_code:
            short_code = URLService._generate_unique_short_code(db, original_url)
        
        try:
            expires_at = datetime.now(timezone.utc) + timedelta(days=expires_in_days)
            new_url = URL(long_url=original_url, short_code=short_code, expires_at=expires_at)
            db.add(new_url)
            db.commit()
            db.refresh(new_url)
            return new_url
            
        except IntegrityError as e:
            db.rollback()
            
            error_str = str(e)
            
            if "ix_urls_long_url" in error_str:
                # Find existing URL and return it via exception
                existing_url = db.query(URL).filter(URL.long_url == original_url).first()
                raise URLAlreadyExistsError(existing_url)
            
            elif "ix_urls_short_code" in error_str:
                raise ShortCodeAlreadyExistsError("Custom alias already exists")
            
            # Re-raise for other integrity errors
            raise
    
    @staticmethod
    def _generate_unique_short_code(db: Session, original_url: str, max_attempts=10):
        from app.models.url import URL
        
        for _ in range(max_attempts):
            # Use entropy-based generation with URL input for better uniqueness
            code = generate_entropy_code(original_url)
            # Check if code already exists
            existing = db.query(URL).filter(URL.short_code == code).first()
            if not existing:
                return code
        
        # If we can't find a unique code after max_attempts, use longer code
        return generate_entropy_code(original_url, length=8)
    
    @staticmethod
    def get_urls_paginated(db: Session, page: int, limit: int):
        from app.models.url import URL
        
        offset = (page - 1) * limit
        
        # Get total count
        total = db.query(URL).count()
        
        # Get paginated results
        urls = db.query(URL).offset(offset).limit(limit).all()
        
        return urls, total
    
    @staticmethod
    def delete_url(db: Session, short_code: str = None, long_url: str = None):
        from app.models.url import URL
        from app.services.cache_service import CacheService
        
        query = db.query(URL)
        
        if short_code:
            query = query.filter(URL.short_code == short_code)
        elif long_url:
            query = query.filter(URL.long_url == long_url)
        
        url = query.first()
        
        if url:
            CacheService.invalidate_cache(url.short_code)
            db.delete(url)
            db.commit()
            return True
        
        return False
    
    @staticmethod
    def get_url_by_short_code(db: Session, short_code: str):
        from app.services.cache_service import CacheService
        from app.models.url import URL
        
        # Try cache first
        cached_data = CacheService.get_url_from_cache(short_code)
        if cached_data:
            # Convert cached dict back to URL-like object
            class CachedURL:
                def __init__(self, data):
                    self.long_url = data['long_url']
                    self.short_code = data['short_code']
                    self.expires_at = data.get('expires_at')
            
            return CachedURL(cached_data)
        
        # If not in cache, query database
        url = db.query(URL).filter(URL.short_code == short_code).first()
        if not url:
            return None
        
        # Check expiration
        if url.expires_at:
            expires_at = url.expires_at
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)
            
            if datetime.now(timezone.utc) > expires_at:
                return None
        
        # Cache the result
        CacheService.cache_url(short_code, url)
        return url