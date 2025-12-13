import orjson
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
                return orjson.loads(cached_data)
        except Exception:
            pass  # Fail silently, fallback to database
        return None
    
    @staticmethod
    def cache_url(short_code: str, url_data):
        """Cache URL data in Redis with pipeline for better performance"""
        try:
            if url_data:
                redis_client = get_redis()
                cache_data = {
                    'long_url': url_data.long_url,
                    'short_code': url_data.short_code,
                    'expires_at': str(url_data.expires_at) if url_data.expires_at else None
                }
                
                # Use pipeline for atomic operations
                pipe = redis_client.pipeline()
                pipe.setex(
                    f"url:{short_code}",
                    settings.CACHE_TTL,
                    orjson.dumps(cache_data)
                )
                # Also cache reverse lookup for analytics
                pipe.setex(
                    f"reverse:{hash(url_data.long_url)}",
                    settings.CACHE_TTL // 2,
                    short_code
                )
                pipe.execute()
        except Exception:
            pass  # Fail silently
    
    @staticmethod
    def invalidate_cache(short_code: str):
        """Remove URL from cache with pipeline"""
        try:
            redis_client = get_redis()
            pipe = redis_client.pipeline()
            pipe.delete(f"url:{short_code}")
            pipe.execute()
        except Exception:
            pass  # Fail silently