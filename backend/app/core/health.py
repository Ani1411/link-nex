import logging
from sqlalchemy import text
from app.database.database import SessionLocal
from app.core.config import settings

logger = logging.getLogger(__name__)

def check_database_connection():
    """Check if database is connected and accessible"""
    try:
        db = SessionLocal()
        # Simple query to test connection
        db.execute(text("SELECT 1"))
        db.close()
        logger.info("Database connection: SUCCESS")
        return True
    except Exception as e:
        logger.error(f"Database connection: FAILED - {str(e)}")
        return False

def check_redis_connection():
    """Check if Redis is connected and accessible"""
    try:
        import redis
        redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        # Test Redis connection
        redis_client.ping()
        logger.info("Redis connection: SUCCESS")
        return True
    except Exception as e:
        logger.error(f"Redis connection: FAILED - {str(e)}")
        return False

def startup_health_check():
    """Run all health checks on startup"""
    logger.info("Starting URL Shortener Application...")
    logger.info("-" * 50)
    
    # Check database
    db_status = check_database_connection()
    
    # Check Redis
    redis_status = check_redis_connection()
    
    logger.info("-" * 50)
    
    if db_status and redis_status:
        logger.info("All services are UP and RUNNING!")
    else:
        logger.warning("Some services are DOWN - check logs above")
    
    logger.info("-" * 50)
    
    return db_status, redis_status