from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.url import URLCreate, URLResponse
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
        # Return existing URL instead of error
        return URLResponse(
            short_url=f"http://localhost:8000/{e.existing_url.short_code}",
            original_url=e.existing_url.long_url,
            expires_at=str(e.existing_url.expires_at) if e.existing_url.expires_at else None
        )
    
    except ShortCodeAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Custom alias already exists. Please choose a different one.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")