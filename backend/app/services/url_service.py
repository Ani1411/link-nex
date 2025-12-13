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
    def _generate_unique_short_code(db: Session, original_url: str, max_attempts=5):
        from app.models.url import URL
        
        for i in range(max_attempts):
            code = generate_entropy_code(original_url + str(i)) if i > 0 else generate_entropy_code(original_url)
            
            # Batch check for better performance
            existing = db.query(URL.short_code).filter(URL.short_code == code).first()
            if not existing:
                return code
        
        # Fallback with timestamp
        return generate_entropy_code(original_url + str(int(datetime.now().timestamp())), length=8)
    
    @staticmethod
    def get_urls_paginated(db: Session, page: int, limit: int):
        from app.models.url import URL
        
        offset = (page - 1) * limit
        
        # Optimized query with select only needed fields
        urls = db.query(URL).order_by(URL.created_at.desc()).offset(offset).limit(limit).all()
        
        # Only count if needed (expensive operation)
        total = db.query(URL).count() if page == 1 else None
        
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
            class CachedURL:
                def __init__(self, data):
                    self.long_url = data['long_url']
                    self.short_code = data['short_code']
                    self.expires_at = data.get('expires_at')
            return CachedURL(cached_data)
        
        # Optimized query - select only needed fields
        url = db.query(URL.long_url, URL.short_code, URL.expires_at).filter(URL.short_code == short_code).first()
        if not url:
            return None
        
        # Check expiration
        if url.expires_at and datetime.now(timezone.utc) > url.expires_at.replace(tzinfo=timezone.utc):
            return None
        
        # Create URL-like object
        class URLResult:
            def __init__(self, long_url, short_code, expires_at):
                self.long_url = long_url
                self.short_code = short_code
                self.expires_at = expires_at
        
        result = URLResult(url.long_url, url.short_code, url.expires_at)
        CacheService.cache_url(short_code, result)
        return result