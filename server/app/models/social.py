from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class SocialPlatform(str, enum.Enum):
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    SPOTIFY = "spotify"
    LINKEDIN = "linkedin"


class SocialConnection(Base):
    __tablename__ = "social_connections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    platform = Column(SQLEnum(SocialPlatform), nullable=False)
    platform_user_id = Column(String(255))
    platform_username = Column(String(255))
    access_token = Column(Text)  # Encrypted in production
    refresh_token = Column(Text)

    # Cached profile data
    profile_data = Column(JSON)  # Platform-specific data

    # Instagram specific
    follower_count = Column(Integer)
    following_count = Column(Integer)
    post_count = Column(Integer)
    bio = Column(Text)

    # Last sync
    last_synced_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="social_connections")
