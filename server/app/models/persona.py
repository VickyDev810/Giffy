from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class VibeTags(Base):
    __tablename__ = "vibe_tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    category = Column(String(50))  # humor, lifestyle, interests, etc.
    description = Column(Text)


class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    # Basic preferences
    budget_preference = Column(String(20))  # low, medium, high, yolo
    gift_style = Column(String(50))  # funny, thoughtful, chaotic, practical

    # Vibe tags stored as JSON array
    vibe_tags = Column(JSON, default=list)  # ["memer", "foodie", "techie"]

    # Interests and preferences
    interests = Column(JSON, default=list)  # ["gaming", "anime", "coffee"]
    dislikes = Column(JSON, default=list)  # ["spicy food", "loud colors"]

    # Size info for wearables
    shirt_size = Column(String(10))
    shoe_size = Column(String(10))

    # Address for delivery
    default_address = Column(Text)
    city = Column(String(100))
    pincode = Column(String(10))

    # AI-generated summary from social data
    ai_summary = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="persona")
