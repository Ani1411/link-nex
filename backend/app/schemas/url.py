from pydantic import BaseModel
from typing import List


class URLCreate(BaseModel):
    original_url: str
    custom_alias: str | None = None
    expires_in_days: int = 30
    

class URLResponse(BaseModel):
    short_url: str
    original_url: str
    expires_at: str | None = None


class URLListResponse(BaseModel):
    urls: List[URLResponse]
    total: int
    page: int
    limit: int
    total_pages: int
