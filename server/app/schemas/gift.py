from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.gift import GiftStatus, DeliveryPlatform


class GiftCreate(BaseModel):
    recipient_id: int
    vibe_prompt: str
    budget_min: float = 0
    budget_max: float
    is_surprise: bool = False  # YOLO mode
    sender_message: Optional[str] = None
    delivery_address: Optional[str] = None


class GiftResponse(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    vibe_prompt: Optional[str]
    budget_min: float
    budget_max: float
    gift_name: Optional[str]
    gift_description: Optional[str]
    gift_image_url: Optional[str]
    gift_price: Optional[float]
    gift_url: Optional[str]
    agent_reasoning: Optional[str]
    platform: Optional[DeliveryPlatform]
    order_id: Optional[str]
    tracking_url: Optional[str]
    delivery_address: Optional[str]
    status: GiftStatus
    is_surprise: bool
    sender_message: Optional[str]
    recipient_reaction: Optional[str]
    created_at: datetime
    ordered_at: Optional[datetime]
    delivered_at: Optional[datetime]
    sender_username: Optional[str] = None
    recipient_username: Optional[str] = None

    class Config:
        from_attributes = True


class GiftApproval(BaseModel):
    approved: bool


class GiftReaction(BaseModel):
    reaction: str


class GiftSubscriptionCreate(BaseModel):
    recipient_id: int
    frequency: str  # daily, weekly, monthly
    day_of_week: Optional[int] = None  # 0-6 for weekly
    day_of_month: Optional[int] = None  # 1-31 for monthly
    time_of_day: str = "10:00"
    vibe_prompt: str
    budget_min: float = 0
    budget_max: float


class GiftSubscriptionResponse(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    frequency: str
    day_of_week: Optional[int]
    day_of_month: Optional[int]
    time_of_day: str
    vibe_prompt: Optional[str]
    budget_min: float
    budget_max: float
    is_active: bool
    last_sent_at: Optional[datetime]
    next_send_at: Optional[datetime]
    total_gifts_sent: int
    created_at: datetime
    recipient_username: Optional[str] = None

    class Config:
        from_attributes = True


class GiftSubscriptionUpdate(BaseModel):
    is_active: Optional[bool] = None
    vibe_prompt: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    frequency: Optional[str] = None
    day_of_week: Optional[int] = None
    day_of_month: Optional[int] = None
    time_of_day: Optional[str] = None
