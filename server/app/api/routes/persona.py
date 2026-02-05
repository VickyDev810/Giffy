from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.persona import Persona, VibeTags
from app.models.friend import Friendship
from app.schemas.persona import PersonaCreate, PersonaUpdate, PersonaResponse, VibeTagResponse

router = APIRouter()


@router.get("/me", response_model=PersonaResponse)
async def get_my_persona(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's persona"""
    persona = db.query(Persona).filter(Persona.user_id == current_user.id).first()
    if not persona:
        # Create default persona if doesn't exist
        persona = Persona(user_id=current_user.id)
        db.add(persona)
        db.commit()
        db.refresh(persona)
    return persona


@router.put("/me", response_model=PersonaResponse)
async def update_my_persona(
    persona_data: PersonaUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's persona"""
    persona = db.query(Persona).filter(Persona.user_id == current_user.id).first()
    if not persona:
        persona = Persona(user_id=current_user.id)
        db.add(persona)

    update_data = persona_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(persona, key, value)

    db.commit()
    db.refresh(persona)
    return persona


@router.get("/friend/{friend_id}", response_model=PersonaResponse)
async def get_friend_persona(
    friend_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a friend's persona (must be friends)"""
    # Verify friendship
    friendship = db.query(Friendship).filter(
        Friendship.user_id == current_user.id,
        Friendship.friend_id == friend_id
    ).first()

    if not friendship:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view personas of your friends"
        )

    persona = db.query(Persona).filter(Persona.user_id == friend_id).first()
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Persona not found"
        )

    return persona


@router.get("/vibe-tags", response_model=List[VibeTagResponse])
async def get_vibe_tags(
    category: str = None,
    db: Session = Depends(get_db)
):
    """Get all available vibe tags"""
    query = db.query(VibeTags)
    if category:
        query = query.filter(VibeTags.category == category)
    return query.all()


@router.post("/vibe-tags", response_model=VibeTagResponse, status_code=status.HTTP_201_CREATED)
async def create_vibe_tag(
    name: str,
    category: str = None,
    description: str = None,
    db: Session = Depends(get_db)
):
    """Create a new vibe tag (admin)"""
    existing = db.query(VibeTags).filter(VibeTags.name == name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vibe tag already exists"
        )

    tag = VibeTags(name=name, category=category, description=description)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@router.post("/me/vibe-tags/{tag_name}")
async def add_vibe_tag_to_persona(
    tag_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a vibe tag to current user's persona"""
    persona = db.query(Persona).filter(Persona.user_id == current_user.id).first()
    if not persona:
        persona = Persona(user_id=current_user.id, vibe_tags=[])
        db.add(persona)

    if persona.vibe_tags is None:
        persona.vibe_tags = []

    if tag_name not in persona.vibe_tags:
        persona.vibe_tags = persona.vibe_tags + [tag_name]

    db.commit()
    return {"message": f"Added '{tag_name}' to your vibe tags"}


@router.delete("/me/vibe-tags/{tag_name}")
async def remove_vibe_tag_from_persona(
    tag_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a vibe tag from current user's persona"""
    persona = db.query(Persona).filter(Persona.user_id == current_user.id).first()
    if not persona or not persona.vibe_tags:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vibe tag not found in your persona"
        )

    if tag_name in persona.vibe_tags:
        new_tags = [t for t in persona.vibe_tags if t != tag_name]
        persona.vibe_tags = new_tags
        db.commit()

    return {"message": f"Removed '{tag_name}' from your vibe tags"}
