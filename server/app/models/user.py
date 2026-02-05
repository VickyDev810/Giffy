from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    phone = Column(String(20))
    avatar_url = Column(Text)
    bio = Column(Text)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    persona = relationship("Persona", back_populates="user", uselist=False)
    social_connections = relationship("SocialConnection", back_populates="user")
    sent_gifts = relationship("Gift", foreign_keys="Gift.sender_id", back_populates="sender")
    received_gifts = relationship("Gift", foreign_keys="Gift.recipient_id", back_populates="recipient")
    gift_subscriptions = relationship("GiftSubscription", foreign_keys="GiftSubscription.sender_id", back_populates="sender")
