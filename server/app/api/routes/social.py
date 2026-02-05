from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.social import SocialConnection, SocialPlatform
from app.models.persona import Persona
from app.services.instagram_service import InstagramService
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class SocialConnectionResponse(BaseModel):
    id: int
    platform: SocialPlatform
    platform_username: Optional[str]
    follower_count: Optional[int]
    following_count: Optional[int]
    post_count: Optional[int]
    bio: Optional[str]
    last_synced_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class InstagramConnectRequest(BaseModel):
    username: str


class InstagramProfileResponse(BaseModel):
    username: str
    full_name: Optional[str]
    bio: Optional[str]
    follower_count: int
    following_count: int
    post_count: int
    is_private: bool
    profile_pic_url: Optional[str]
    recent_posts: List[dict] = []


@router.get("/connections", response_model=List[SocialConnectionResponse])
async def get_social_connections(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all social connections for current user"""
    connections = db.query(SocialConnection).filter(
        SocialConnection.user_id == current_user.id
    ).all()
    return connections


@router.post("/instagram/connect", response_model=SocialConnectionResponse)
async def connect_instagram(
    request: InstagramConnectRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Connect Instagram account by username (public profile fetch)"""
    # Check if already connected
    existing = db.query(SocialConnection).filter(
        SocialConnection.user_id == current_user.id,
        SocialConnection.platform == SocialPlatform.INSTAGRAM
    ).first()

    if existing:
        # Update username
        existing.platform_username = request.username
        existing.last_synced_at = None  # Will be updated after sync
        db.commit()
        connection = existing
    else:
        # Create new connection
        connection = SocialConnection(
            user_id=current_user.id,
            platform=SocialPlatform.INSTAGRAM,
            platform_username=request.username
        )
        db.add(connection)
        db.commit()
        db.refresh(connection)

    # Trigger background sync
    background_tasks.add_task(
        InstagramService.sync_profile,
        connection_id=connection.id,
        db_url=str(db.get_bind().url)
    )

    return connection


@router.post("/instagram/sync")
async def sync_instagram(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Manually trigger Instagram profile sync"""
    connection = db.query(SocialConnection).filter(
        SocialConnection.user_id == current_user.id,
        SocialConnection.platform == SocialPlatform.INSTAGRAM
    ).first()

    if not connection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instagram not connected"
        )

    background_tasks.add_task(
        InstagramService.sync_profile,
        connection_id=connection.id,
        db_url=str(db.get_bind().url)
    )

    return {"message": "Sync started"}


@router.get("/instagram/profile/{username}", response_model=InstagramProfileResponse)
async def get_instagram_profile(
    username: str,
    current_user: User = Depends(get_current_user),
):
    """Fetch public Instagram profile data"""
    profile = await InstagramService.fetch_profile(username)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found or private"
        )
    return profile


@router.delete("/instagram", status_code=status.HTTP_204_NO_CONTENT)
async def disconnect_instagram(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Disconnect Instagram account"""
    db.query(SocialConnection).filter(
        SocialConnection.user_id == current_user.id,
        SocialConnection.platform == SocialPlatform.INSTAGRAM
    ).delete()
    db.commit()
    return None


@router.post("/instagram/analyze-for-gifts")
async def analyze_instagram_for_gifts(
    username: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze Instagram profile to suggest gift ideas"""
    analysis = await InstagramService.analyze_for_gifts(username)
    return analysis
