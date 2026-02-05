from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PersonaCreate(BaseModel):
    budget_preference: Optional[str] = "medium"
    gift_style: Optional[str] = "thoughtful"
    vibe_tags: Optional[List[str]] = []
    interests: Optional[List[str]] = []
    dislikes: Optional[List[str]] = []
    shirt_size: Optional[str] = None
    shoe_size: Optional[str] = None
    default_address: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None


class PersonaUpdate(BaseModel):
    budget_preference: Optional[str] = None
    gift_style: Optional[str] = None
    vibe_tags: Optional[List[str]] = None
    interests: Optional[List[str]] = None
    dislikes: Optional[List[str]] = None
    shirt_size: Optional[str] = None
    shoe_size: Optional[str] = None
    default_address: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None


class PersonaResponse(BaseModel):
    id: int
    user_id: int
    budget_preference: Optional[str]
    gift_style: Optional[str]
    vibe_tags: List[str]
    interests: List[str]
    dislikes: List[str]
    shirt_size: Optional[str]
    shoe_size: Optional[str]
    default_address: Optional[str]
    city: Optional[str]
    pincode: Optional[str]
    ai_summary: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class VibeTagResponse(BaseModel):
    id: int
    name: str
    category: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True
