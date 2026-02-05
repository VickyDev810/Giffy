from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.friend import FriendRequest, Friendship, FriendRequestStatus
from app.schemas.friend import (
    FriendRequestCreate,
    FriendRequestResponse,
    FriendshipResponse,
    FriendRequestAction,
    SetNicknameRequest,
)

router = APIRouter()


@router.post("/request", response_model=FriendRequestResponse, status_code=status.HTTP_201_CREATED)
async def send_friend_request(
    request_data: FriendRequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a friend request"""
    if request_data.receiver_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot send friend request to yourself"
        )

    # Check if receiver exists
    receiver = db.query(User).filter(User.id == request_data.receiver_id).first()
    if not receiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check if already friends
    existing_friendship = db.query(Friendship).filter(
        ((Friendship.user_id == current_user.id) & (Friendship.friend_id == request_data.receiver_id)) |
        ((Friendship.user_id == request_data.receiver_id) & (Friendship.friend_id == current_user.id))
    ).first()

    if existing_friendship:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already friends"
        )

    # Check if request already exists
    existing_request = db.query(FriendRequest).filter(
        FriendRequest.sender_id == current_user.id,
        FriendRequest.receiver_id == request_data.receiver_id,
        FriendRequest.status == FriendRequestStatus.PENDING
    ).first()

    if existing_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Friend request already sent"
        )

    # Check for reverse request (they sent us one)
    reverse_request = db.query(FriendRequest).filter(
        FriendRequest.sender_id == request_data.receiver_id,
        FriendRequest.receiver_id == current_user.id,
        FriendRequest.status == FriendRequestStatus.PENDING
    ).first()

    if reverse_request:
        # Auto-accept if they already sent us a request
        reverse_request.status = FriendRequestStatus.ACCEPTED
        # Create mutual friendship
        friendship1 = Friendship(user_id=current_user.id, friend_id=request_data.receiver_id)
        friendship2 = Friendship(user_id=request_data.receiver_id, friend_id=current_user.id)
        db.add_all([friendship1, friendship2])
        db.commit()
        db.refresh(reverse_request)

        response = FriendRequestResponse.model_validate(reverse_request)
        response.sender_username = receiver.username
        response.receiver_username = current_user.username
        return response

    # Create new request
    friend_request = FriendRequest(
        sender_id=current_user.id,
        receiver_id=request_data.receiver_id,
        message=request_data.message
    )
    db.add(friend_request)
    db.commit()
    db.refresh(friend_request)

    response = FriendRequestResponse.model_validate(friend_request)
    response.sender_username = current_user.username
    response.receiver_username = receiver.username
    return response


@router.get("/requests/incoming", response_model=List[FriendRequestResponse])
async def get_incoming_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get pending friend requests received"""
    requests = db.query(FriendRequest).filter(
        FriendRequest.receiver_id == current_user.id,
        FriendRequest.status == FriendRequestStatus.PENDING
    ).all()

    result = []
    for req in requests:
        sender = db.query(User).filter(User.id == req.sender_id).first()
        response = FriendRequestResponse.model_validate(req)
        response.sender_username = sender.username if sender else None
        result.append(response)

    return result


@router.get("/requests/outgoing", response_model=List[FriendRequestResponse])
async def get_outgoing_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get pending friend requests sent"""
    requests = db.query(FriendRequest).filter(
        FriendRequest.sender_id == current_user.id,
        FriendRequest.status == FriendRequestStatus.PENDING
    ).all()

    result = []
    for req in requests:
        receiver = db.query(User).filter(User.id == req.receiver_id).first()
        response = FriendRequestResponse.model_validate(req)
        response.receiver_username = receiver.username if receiver else None
        result.append(response)

    return result


@router.post("/requests/{request_id}/respond", response_model=FriendRequestResponse)
async def respond_to_request(
    request_id: int,
    action: FriendRequestAction,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Accept or reject a friend request"""
    friend_request = db.query(FriendRequest).filter(
        FriendRequest.id == request_id,
        FriendRequest.receiver_id == current_user.id,
        FriendRequest.status == FriendRequestStatus.PENDING
    ).first()

    if not friend_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Friend request not found"
        )

    if action.action == "accept":
        friend_request.status = FriendRequestStatus.ACCEPTED
        # Create mutual friendship
        friendship1 = Friendship(user_id=current_user.id, friend_id=friend_request.sender_id)
        friendship2 = Friendship(user_id=friend_request.sender_id, friend_id=current_user.id)
        db.add_all([friendship1, friendship2])
    elif action.action == "reject":
        friend_request.status = FriendRequestStatus.REJECTED
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid action. Use 'accept' or 'reject'"
        )

    db.commit()
    db.refresh(friend_request)
    return friend_request


@router.get("/", response_model=List[FriendshipResponse])
async def get_friends(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all friends"""
    friendships = db.query(Friendship).filter(
        Friendship.user_id == current_user.id
    ).all()

    result = []
    for friendship in friendships:
        friend = db.query(User).filter(User.id == friendship.friend_id).first()
        response = FriendshipResponse.model_validate(friendship)
        if friend:
            response.friend_username = friend.username
            response.friend_full_name = friend.full_name
            response.friend_avatar_url = friend.avatar_url
        result.append(response)

    return result


@router.put("/{friend_id}/nickname", response_model=FriendshipResponse)
async def set_friend_nickname(
    friend_id: int,
    nickname_data: SetNicknameRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Set a nickname for a friend"""
    friendship = db.query(Friendship).filter(
        Friendship.user_id == current_user.id,
        Friendship.friend_id == friend_id
    ).first()

    if not friendship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Friendship not found"
        )

    friendship.nickname = nickname_data.nickname
    db.commit()
    db.refresh(friendship)

    friend = db.query(User).filter(User.id == friend_id).first()
    response = FriendshipResponse.model_validate(friendship)
    if friend:
        response.friend_username = friend.username
        response.friend_full_name = friend.full_name
        response.friend_avatar_url = friend.avatar_url

    return response


@router.delete("/{friend_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_friend(
    friend_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a friend (unfriend)"""
    # Delete both friendship records
    db.query(Friendship).filter(
        ((Friendship.user_id == current_user.id) & (Friendship.friend_id == friend_id)) |
        ((Friendship.user_id == friend_id) & (Friendship.friend_id == current_user.id))
    ).delete(synchronize_session=False)

    db.commit()
    return None
