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