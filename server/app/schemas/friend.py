from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.friend import FriendRequestStatus


class FriendRequestCreate(BaseModel):
    receiver_id: int
    message: Optional[str] = None


class FriendRequestResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    status: FriendRequestStatus
    message: Optional[str]
    created_at: datetime
    sender_username: Optional[str] = None
    receiver_username: Optional[str] = None

    class Config:
        from_attributes = True


class FriendRequestAction(BaseModel):
    action: str  # "accept" or "reject"


class FriendshipResponse(BaseModel):
    id: int
    user_id: int
    friend_id: int
    nickname: Optional[str]
    created_at: datetime
    friend_username: Optional[str] = None
    friend_full_name: Optional[str] = None
    friend_avatar_url: Optional[str] = None

    class Config:
        from_attributes = True


class SetNicknameRequest(BaseModel):
    nickname: str
