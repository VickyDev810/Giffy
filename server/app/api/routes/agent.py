"""
Agent API Routes
Provides endpoints for communicating with the Blinkit Chaos Agent
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import json
import asyncio

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.blinkit_chaos_agent import BlinkitChaosAgentService

router = APIRouter()


# Request/Response Models
class ChatMessage(BaseModel):
    message: str


class SessionResponse(BaseModel):
    session_id: str
    user_id: int
    created_at: datetime
    message_count: int

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    role: str
    content: str
    timestamp: str


class SessionHistoryResponse(BaseModel):
    session_id: str
    messages: List[MessageResponse]


class ChatStartRequest(BaseModel):
    """Request to start a new chaos agent session with optional initial message"""
    vibe_prompt: Optional[str] = None
    budget_min: Optional[float] = 0
    budget_max: Optional[float] = 1000
    recipient_name: Optional[str] = None


@router.post("/sessions", response_model=SessionResponse)
async def create_agent_session(
    request: Optional[ChatStartRequest] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new Blinkit Chaos Agent session.
    Optionally provide context about the gift to help the agent.
    """
    try:
        session = await BlinkitChaosAgentService.create_session(user_id=current_user.id)

        # If initial context provided, send it as first message
        if request and (request.vibe_prompt or request.recipient_name):
            context_msg = f"I want to send a chaotic gift"
            if request.recipient_name:
                context_msg += f" to {request.recipient_name}"
            if request.vibe_prompt:
                context_msg += f". The vibe should be: {request.vibe_prompt}"
            context_msg += f". Budget: Rs.{request.budget_min} - Rs.{request.budget_max}"

            # Prime the agent with context (don't stream this)
            chunks = []
            async for chunk in session.chat(context_msg):
                chunks.append(chunk)

        return SessionResponse(
            session_id=session.session_id,
            user_id=session.user_id,
            created_at=session.created_at,
            message_count=len(session.messages)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create agent session: {str(e)}"
        )


@router.get("/sessions", response_model=List[SessionResponse])
async def list_agent_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all active agent sessions for the current user"""
    sessions = BlinkitChaosAgentService.get_user_sessions(current_user.id)

    return [
        SessionResponse(
            session_id=s.session_id,
            user_id=s.user_id,
            created_at=s.created_at,
            message_count=len(s.messages)
        )
        for s in sessions
    ]


@router.get("/sessions/{session_id}", response_model=SessionHistoryResponse)
async def get_session_history(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get chat history for a session"""
    session = BlinkitChaosAgentService.get_session(session_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    if session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this session"
        )

    return SessionHistoryResponse(
        session_id=session.session_id,
        messages=[
            MessageResponse(
                role=m["role"],
                content=m["content"],
                timestamp=m["timestamp"]
            )
            for m in session.messages
        ]
    )


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an agent session"""
    session = BlinkitChaosAgentService.get_session(session_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    if session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this session"
        )

    await BlinkitChaosAgentService.delete_session(session_id)
    return None


@router.post("/sessions/{session_id}/chat")
async def chat_with_agent(
    session_id: str,
    chat: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send a message to the chaos agent and get a streaming response.
    Returns Server-Sent Events (SSE) for real-time streaming.
    """
    session = BlinkitChaosAgentService.get_session(session_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    if session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this session"
        )

    async def generate_stream():
        """Generate SSE stream from agent response"""
        try:
            async for chunk in session.chat(chat.message):
                # Format as SSE
                data = json.dumps({"type": "chunk", "content": chunk})
                yield f"data: {data}\n\n"

            # Send completion event
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
        except Exception as e:
            error_data = json.dumps({"type": "error", "content": str(e)})
            yield f"data: {error_data}\n\n"

    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@router.post("/sessions/{session_id}/chat/sync", response_model=MessageResponse)
async def chat_with_agent_sync(
    session_id: str,
    chat: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send a message to the chaos agent and get a complete response.
    Non-streaming endpoint for simpler clients.
    """
    session = BlinkitChaosAgentService.get_session(session_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    if session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this session"
        )

    try:
        full_response = ""
        async for chunk in session.chat(chat.message):
            full_response += chunk

        return MessageResponse(
            role="assistant",
            content=full_response,
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent error: {str(e)}"
        )


# Quick action endpoints
@router.post("/chaos-gift")
async def quick_chaos_gift(
    request: ChatStartRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Quick endpoint to start a chaos gift flow.
    Creates session and returns initial agent response with session details.
    """
    try:
        # Create session
        session = await BlinkitChaosAgentService.create_session(user_id=current_user.id)

        # Build initial prompt
        prompt = f"Help me send a chaotic surprise gift!"
        if request.recipient_name:
            prompt = f"Help me send a chaotic surprise gift to {request.recipient_name}!"
        if request.vibe_prompt:
            prompt += f" The vibe I want is: {request.vibe_prompt}."
        prompt += f" My budget is between Rs.{request.budget_min} and Rs.{request.budget_max}."
        prompt += " Let's do this!"

        # Get initial response
        initial_response = ""
        async for chunk in session.chat(prompt):
            initial_response += chunk

        return {
            "session_id": session.session_id,
            "initial_prompt": prompt,
            "agent_response": initial_response,
            "message": "Chaos agent session started! Continue chatting to complete your gift order."
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start chaos gift: {str(e)}"
        )
