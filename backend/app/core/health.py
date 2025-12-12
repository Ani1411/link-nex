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

def get_database_health():
    """Get comprehensive database health information"""
    import time
    from app.database.database import engine
    
    health_data = {
        "status": "unknown",
        "connection": False,
        "response_time_ms": None,
        "pool_status": {},
        "database_info": {},
        "table_stats": {},
        "error": None
    }
    
    try:
        db = SessionLocal()
        start_time = time.time()
        
        # Test basic connection
        db.execute(text("SELECT 1"))
        response_time = (time.time() - start_time) * 1000
        
        health_data["connection"] = True
        health_data["response_time_ms"] = round(response_time, 2)
        
        # Get database version and info
        version_result = db.execute(text("SELECT version()")).fetchone()
        health_data["database_info"] = {
            "version": version_result[0] if version_result else "Unknown",
            "database_name": db.execute(text("SELECT current_database()")).fetchone()[0]
        }
        
        # Get connection pool status
        pool = engine.pool
        health_data["pool_status"] = {
            "pool_size": pool.size(),
            "checked_in": pool.checkedin(),
            "checked_out": pool.checkedout(),
            "overflow": pool.overflow(),
            "invalid": pool.invalid()
        }
        
        db.close()
        
        # Determine overall status
        if response_time < 100:
            health_data["status"] = "excellent"
        elif response_time < 500:
            health_data["status"] = "good"
        elif response_time < 1000:
            health_data["status"] = "fair"
        else:
            health_data["status"] = "slow"
            
    except Exception as e:
        health_data["status"] = "unhealthy"
        health_data["error"] = str(e)
    
    return health_data