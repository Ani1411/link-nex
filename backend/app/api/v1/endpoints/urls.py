from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.schemas.url import URLCreate, URLResponse, URLListResponse
from app.services.url_service import URLService, URLAlreadyExistsError, ShortCodeAlreadyExistsError
from app.database.database import get_db

router = APIRouter()


@router.post("/create", response_model=URLResponse, tags=["urls"])
def create_url(url_data: URLCreate, db: Session = Depends(get_db)):
    try:
        url_obj = URLService.create_short_url(
            db=db,
            original_url=url_data.original_url, 
            short_code=url_data.custom_alias,
            expires_in_days=url_data.expires_in_days
        )

        return URLResponse(
            short_url=f"http://localhost:8000/{url_obj.short_code}",
            original_url=url_obj.long_url,
            expires_at=str(url_obj.expires_at) if url_obj.expires_at else None
        )
        
    except URLAlreadyExistsError as e:
        # Check if custom alias was provided
        if url_data.custom_alias:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail={
                    "message": f"URL already shortened. Existing short code: {e.existing_url.short_code}",
                    "existing_url": {
                        "short_url": f"http://localhost:8000/{e.existing_url.short_code}",
                        "original_url": e.existing_url.long_url,
                        "expires_at": str(e.existing_url.expires_at) if e.existing_url.expires_at else None
                    }
                }
            )
        else:
            # Return existing URL for auto-generated codes
            return URLResponse(
                short_url=f"http://localhost:8000/{e.existing_url.short_code}",
                original_url=e.existing_url.long_url,
                expires_at=str(e.existing_url.expires_at) if e.existing_url.expires_at else None
            )
    
    except ShortCodeAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Custom alias already exists. Please choose a different one.")
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {str(e)}")


@router.get("/list", response_model=URLListResponse, tags=["urls"])
def list_urls(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page")
):
    """List all URLs with pagination"""
    try:
        urls, total = URLService.get_urls_paginated(db, page, limit)
        
        url_responses = [
            URLResponse(
                short_url=f"http://localhost:8000/{url.short_code}",
                original_url=url.long_url,
                expires_at=str(url.expires_at) if url.expires_at else None
            )
            for url in urls
        ]
        
        return URLListResponse(
            urls=url_responses,
            total=total,
            page=page,
            limit=limit,
            total_pages=(total + limit - 1) // limit
        )
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {str(e)}")


@router.delete("/delete", tags=["urls"])
def delete_url(
    short_code: str = Query(None, description="Short code to delete"),
    long_url: str = Query(None, description="Long URL to delete"),
    db: Session = Depends(get_db)
):
    """Delete URL by short code or long URL"""
    if not short_code and not long_url:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Either short_code or long_url must be provided")
    
    try:
        deleted = URLService.delete_url(db, short_code, long_url)
        
        if deleted:
            return {"message": "URL deleted successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")
            
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {str(e)}")