from app.database.database import Base
from sqlalchemy import Column, UUID, String, DateTime
from sqlalchemy.sql import func
from uuid import uuid4


class URL(Base):
    __tablename__ = "urls"
    
    id = Column(UUID, primary_key=True, index=True, default=uuid4)
    long_url = Column(String, nullable=False, unique=True, index=True)
    short_code = Column(String, unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    
    def is_active(self):
        if self.expires_at:
            return func.now() < self.expires_at
        return True
    
    def __repr__(self):
        return f"<URL(id={self.id}, short_code={self.short_code}, long_url={self.long_url})>"
    
    def __str__(self):
        return self.long_url
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "long_url": self.long_url,
            "short_code": self.short_code,
            "expires_at": self.expires_at,
            "created_at": self.created_at,
        }
        
    @classmethod
    def from_dict(cls, data):
        return cls(
            long_url=data.get("long_url"),
            short_code=data.get("short_code"),
            expires_at=data.get("expires_at"),
        )       
        
    @classmethod
    def get_by_short_code(cls, session, short_code):
        return session.query(cls).filter_by(short_code=short_code).first()              
    
    