from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.friend import Friendship
from app.models.persona import Persona
from app.models.gift import Gift, GiftSubscription, GiftStatus
from app.schemas.gift import (
    GiftCreate,
    GiftResponse,
    GiftApproval,
    GiftReaction,
    GiftSubscriptionCreate,
    GiftSubscriptionResponse,
    GiftSubscriptionUpdate,
)
from app.services.gift_agent import GiftAgentService

router = APIRouter()


@router.post("/", response_model=GiftResponse, status_code=status.HTTP_201_CREATED)
async def create_gift(
    gift_data: GiftCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new gift (send to friend)"""
    # Verify friendship
    friendship = db.query(Friendship).filter(
        Friendship.user_id == current_user.id,
        Friendship.friend_id == gift_data.recipient_id
    ).first()

    if not friendship:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only send gifts to your friends"
        )

    # Get recipient's persona for delivery address if not provided
    recipient_persona = db.query(Persona).filter(Persona.user_id == gift_data.recipient_id).first()
    delivery_address = gift_data.delivery_address
    if not delivery_address and recipient_persona:
        delivery_address = recipient_persona.default_address

    # Create gift
    gift = Gift(
        sender_id=current_user.id,
        recipient_id=gift_data.recipient_id,
        vibe_prompt=gift_data.vibe_prompt,
        budget_min=gift_data.budget_min,
        budget_max=gift_data.budget_max,
        is_surprise=gift_data.is_surprise,
        sender_message=gift_data.sender_message,
        delivery_address=delivery_address,
        status=GiftStatus.AGENT_PICKING
    )
    db.add(gift)
    db.commit()
    db.refresh(gift)

    # Trigger agent to pick gift in background
    background_tasks.add_task(
        GiftAgentService.pick_gift,
        gift_id=gift.id,
        db_url=str(db.get_bind().url)
    )

    recipient = db.query(User).filter(User.id == gift_data.recipient_id).first()
    response = GiftResponse.model_validate(gift)
    response.sender_username = current_user.username
    response.recipient_username = recipient.username if recipient else None

    return response


@router.get("/sent", response_model=List[GiftResponse])
async def get_sent_gifts(
    status_filter: GiftStatus = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all gifts sent by current user"""
    query = db.query(Gift).filter(Gift.sender_id == current_user.id)
    if status_filter:
        query = query.filter(Gift.status == status_filter)

    gifts = query.order_by(Gift.created_at.desc()).all()

    result = []
    for gift in gifts:
        recipient = db.query(User).filter(User.id == gift.recipient_id).first()
        response = GiftResponse.model_validate(gift)
        response.sender_username = current_user.username
        response.recipient_username = recipient.username if recipient else None
        result.append(response)

    return result


@router.get("/received", response_model=List[GiftResponse])
async def get_received_gifts(
    status_filter: GiftStatus = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all gifts received by current user"""
    query = db.query(Gift).filter(Gift.recipient_id == current_user.id)
    if status_filter:
        query = query.filter(Gift.status == status_filter)

    gifts = query.order_by(Gift.created_at.desc()).all()

    result = []
    for gift in gifts:
        sender = db.query(User).filter(User.id == gift.sender_id).first()
        response = GiftResponse.model_validate(gift)
        response.sender_username = sender.username if sender else None
        response.recipient_username = current_user.username
        result.append(response)

    return result


@router.get("/{gift_id}", response_model=GiftResponse)
async def get_gift(
    gift_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get gift details"""
    gift = db.query(Gift).filter(Gift.id == gift_id).first()
    if not gift:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gift not found"
        )

    # Only sender or recipient can view
    if gift.sender_id != current_user.id and gift.recipient_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this gift"
        )

    sender = db.query(User).filter(User.id == gift.sender_id).first()
    recipient = db.query(User).filter(User.id == gift.recipient_id).first()

    response = GiftResponse.model_validate(gift)
    response.sender_username = sender.username if sender else None
    response.recipient_username = recipient.username if recipient else None

    return response


@router.post("/{gift_id}/approve", response_model=GiftResponse)
async def approve_gift(
    gift_id: int,
    approval: GiftApproval,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Approve or reject agent's gift selection (sender only)"""
    gift = db.query(Gift).filter(
        Gift.id == gift_id,
        Gift.sender_id == current_user.id,
        Gift.status == GiftStatus.AWAITING_APPROVAL
    ).first()

    if not gift:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gift not found or not awaiting approval"
        )

    if approval.approved:
        gift.status = GiftStatus.ORDERED
        gift.ordered_at = datetime.utcnow()
        # Trigger order in background
        background_tasks.add_task(
            GiftAgentService.place_order,
            gift_id=gift.id,
            db_url=str(db.get_bind().url)
        )
    else:
        gift.status = GiftStatus.CANCELLED

    db.commit()
    db.refresh(gift)
    return gift


@router.post("/{gift_id}/reaction", response_model=GiftResponse)
async def add_reaction(
    gift_id: int,
    reaction: GiftReaction,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add recipient's reaction to gift"""
    gift = db.query(Gift).filter(
        Gift.id == gift_id,
        Gift.recipient_id == current_user.id
    ).first()

    if not gift:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gift not found"
        )

    gift.recipient_reaction = reaction.reaction
    db.commit()
    db.refresh(gift)
    return gift


@router.post("/surprise/{friend_id}", response_model=GiftResponse)
async def surprise_friend(
    friend_id: int,
    budget_max: float,
    background_tasks: BackgroundTasks,
    vibe_prompt: str = "something chaotic and fun",
    budget_min: float = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Quick surprise gift - YOLO mode (no approval needed)"""
    # Verify friendship
    friendship = db.query(Friendship).filter(
        Friendship.user_id == current_user.id,
        Friendship.friend_id == friend_id
    ).first()

    if not friendship:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only surprise your friends"
        )

    # Get recipient's persona for delivery
    recipient_persona = db.query(Persona).filter(Persona.user_id == friend_id).first()
    delivery_address = recipient_persona.default_address if recipient_persona else None

    if not delivery_address:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Friend has no delivery address set"
        )

    # Create surprise gift
    gift = Gift(
        sender_id=current_user.id,
        recipient_id=friend_id,
        vibe_prompt=vibe_prompt,
        budget_min=budget_min,
        budget_max=budget_max,
        is_surprise=True,
        delivery_address=delivery_address,
        status=GiftStatus.AGENT_PICKING
    )
    db.add(gift)
    db.commit()
    db.refresh(gift)

    # Trigger agent
    background_tasks.add_task(
        GiftAgentService.pick_and_order_gift,
        gift_id=gift.id,
        db_url=str(db.get_bind().url)
    )

    return gift


# ==================== SUBSCRIPTIONS ====================

@router.post("/subscriptions", response_model=GiftSubscriptionResponse, status_code=status.HTTP_201_CREATED)
async def create_subscription(
    sub_data: GiftSubscriptionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create automated recurring gift subscription"""
    # Verify friendship
    friendship = db.query(Friendship).filter(
        Friendship.user_id == current_user.id,
        Friendship.friend_id == sub_data.recipient_id
    ).first()

    if not friendship:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only subscribe to gift your friends"
        )

    subscription = GiftSubscription(
        sender_id=current_user.id,
        recipient_id=sub_data.recipient_id,
        frequency=sub_data.frequency,
        day_of_week=sub_data.day_of_week,
        day_of_month=sub_data.day_of_month,
        time_of_day=sub_data.time_of_day,
        vibe_prompt=sub_data.vibe_prompt,
        budget_min=sub_data.budget_min,
        budget_max=sub_data.budget_max,
    )
    db.add(subscription)
    db.commit()
    db.refresh(subscription)

    recipient = db.query(User).filter(User.id == sub_data.recipient_id).first()
    response = GiftSubscriptionResponse.model_validate(subscription)
    response.recipient_username = recipient.username if recipient else None

    return response


@router.get("/subscriptions", response_model=List[GiftSubscriptionResponse])
async def get_subscriptions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all gift subscriptions"""
    subscriptions = db.query(GiftSubscription).filter(
        GiftSubscription.sender_id == current_user.id
    ).all()

    result = []
    for sub in subscriptions:
        recipient = db.query(User).filter(User.id == sub.recipient_id).first()
        response = GiftSubscriptionResponse.model_validate(sub)
        response.recipient_username = recipient.username if recipient else None
        result.append(response)

    return result


@router.put("/subscriptions/{subscription_id}", response_model=GiftSubscriptionResponse)
async def update_subscription(
    subscription_id: int,
    sub_data: GiftSubscriptionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update gift subscription"""
    subscription = db.query(GiftSubscription).filter(
        GiftSubscription.id == subscription_id,
        GiftSubscription.sender_id == current_user.id
    ).first()

    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )

    update_data = sub_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(subscription, key, value)

    db.commit()
    db.refresh(subscription)
    return subscription


@router.delete("/subscriptions/{subscription_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_subscription(
    subscription_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel gift subscription"""
    subscription = db.query(GiftSubscription).filter(
        GiftSubscription.id == subscription_id,
        GiftSubscription.sender_id == current_user.id
    ).first()

    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )

    db.delete(subscription)
    db.commit()
    return None
