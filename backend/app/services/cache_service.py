import json
from typing import Optional
from app.database.redis import get_redis
from app.core.config import settings

class CacheService:
    
    @staticmethod
    def get_url_from_cache(short_code: str) -> Optional[dict]:
        """Get URL data from Redis cache"""
        try:
            redis_client = get_redis()
            cached_data = redis_client.get(f"url:{short_code}")
            
            if cached_data:
                return json.loads(cached_data)
        except Exception:
            pass  # Fail silently, fallback to database
        return None
    
    @staticmethod
    def cache_url(short_code: str, url_data):
        """Cache URL data in Redis"""
        try:
            if url_data:
                redis_client = get_redis()
                cache_data = {
                    'long_url': url_data.long_url,
                    'short_code': url_data.short_code,
                    'expires_at': str(url_data.expires_at) if url_data.expires_at else None
                }
                redis_client.setex(
                    f"url:{short_code}",
                    settings.CACHE_TTL,
                    json.dumps(cache_data)
                )
        except Exception:
            pass  # Fail silently
    
    @staticmethod
    def invalidate_cache(short_code: str):
        """Remove URL from cache"""
        try:
            redis_client = get_redis()
            redis_client.delete(f"url:{short_code}")
        except Exception:
            pass  # Fail silently