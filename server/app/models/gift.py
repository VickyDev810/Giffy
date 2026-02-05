from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Boolean, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class GiftStatus(str, enum.Enum):
    PENDING = "pending"
    AGENT_PICKING = "agent_picking"
    AWAITING_APPROVAL = "awaiting_approval"
    ORDERED = "ordered"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class DeliveryPlatform(str, enum.Enum):
    BLINKIT = "blinkit"
    ZEPTO = "zepto"
    SWIGGY_INSTAMART = "swiggy_instamart"
    AMAZON = "amazon"
    MANUAL = "manual"


class Gift(Base):
    __tablename__ = "gifts"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Gift details
    vibe_prompt = Column(Text)  # "send something chaotic", "roast-worthy"
    budget_min = Column(Float, default=0)
    budget_max = Column(Float, nullable=False)

    # Selected gift info
    gift_name = Column(String(255))
    gift_description = Column(Text)
    gift_image_url = Column(Text)
    gift_price = Column(Float)
    gift_url = Column(Text)

    # Agent reasoning
    agent_reasoning = Column(Text)  # Why the agent picked this gift

    # Delivery info
    platform = Column(SQLEnum(DeliveryPlatform))
    order_id = Column(String(100))
    tracking_url = Column(Text)
    delivery_address = Column(Text)

    # Status
    status = Column(SQLEnum(GiftStatus), default=GiftStatus.PENDING)
    is_surprise = Column(Boolean, default=False)  # True = YOLO mode, no approval needed

    # Message
    sender_message = Column(Text)
    recipient_reaction = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    ordered_at = Column(DateTime(timezone=True))
    delivered_at = Column(DateTime(timezone=True))

    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_gifts")
    recipient = relationship("User", foreign_keys=[recipient_id], back_populates="received_gifts")


class GiftSubscription(Base):
    """For automated recurring gifts"""
    __tablename__ = "gift_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Schedule
    frequency = Column(String(20))  # daily, weekly, monthly
    day_of_week = Column(Integer)  # 0-6 for weekly
    day_of_month = Column(Integer)  # 1-31 for monthly
    time_of_day = Column(String(5))  # HH:MM format

    # Gift preferences
    vibe_prompt = Column(Text)
    budget_min = Column(Float, default=0)
    budget_max = Column(Float, nullable=False)

    # Status
    is_active = Column(Boolean, default=True)
    last_sent_at = Column(DateTime(timezone=True))
    next_send_at = Column(DateTime(timezone=True))
    total_gifts_sent = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    sender = relationship("User", foreign_keys=[sender_id], back_populates="gift_subscriptions")
    recipient = relationship("User", foreign_keys=[recipient_id])
