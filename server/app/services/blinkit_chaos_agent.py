"""
Blinkit Chaos Agent Service
Integrates with the agent_work blinkit agent for chaotic gift procurement
"""
import os
import sys
import asyncio
from typing import AsyncGenerator, Dict, Optional
from datetime import datetime
import logging

# Add agent_work to path
AGENT_WORK_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../agent"))
sys.path.insert(0, AGENT_WORK_PATH)

from build_agent.openrouter import OpenRouterAgent
from runners.stream import StreamAgentRunner
from agent_framework import MCPStdioTool

logger = logging.getLogger(__name__)

# Chaos agent instructions
CHAOS_AGENT_INSTRUCTIONS = """
Identity

You are a Chaotic Procurement Agent for Giftify. Your goal is to execute a high-speed, randomized purchase of a "mood-brightening" gift within a strict budget and specific account parameters.

Capabilities

The optimal flow:
1. Check login status if logged in go to step 3 else start from step 1 wait for confirmation.
2. Ask user the otp. Skip if logged in use this number TEST_MOBILE_NO. to login.
3. Search that chaos product from your mind and users query.
4. Use Complete Checkout function for the selected product. (Just keep in mind the budget constraint).


Rules:
Always follow the flow that is given above to get the most desirable results.
Find the best possible gift according to users vibe.
Be creative and chaotic with gift selections!
Keep responses fun and engaging.
"""


class BlinkitChaosAgentSession:
    """Manages a single chat session with the Blinkit Chaos Agent"""

    def __init__(self, session_id: str, user_id: int):
        self.session_id = session_id
        self.user_id = user_id
        self.created_at = datetime.utcnow()
        self.messages: list = []
        self._agent = None
        self._thread = None
        self._runner = None
        self._mcp_tool = None

    async def initialize(self):
        """Initialize the agent and MCP tool"""
        # Create MCP tool for Blinkit
        self._mcp_tool = MCPStdioTool(
            name="blinkit-mcp",
            command=f"{AGENT_WORK_PATH}/venv/bin/python",
            args=[f"{AGENT_WORK_PATH}/blinkit_mcp_new.py"],
            description="Blinkit Shopping Agent"
        )
        
        # Build the agent
        self._agent = OpenRouterAgent(
            instructions=CHAOS_AGENT_INSTRUCTIONS,
            name="Blinkit Chaos Agent",
            tools=self._mcp_tool,
        ).build_agent()

        # Get a new thread for conversation
        self._thread = self._agent.get_new_thread()
        self._runner = StreamAgentRunner(agent=self._agent, thread=self._thread)

        logger.info(f"Initialized chaos agent session {self.session_id} for user {self.user_id}")

    async def chat(self, message: str) -> AsyncGenerator[str, None]:
        """Send a message and stream the response"""
        if not self._runner:
            await self.initialize()

        self.messages.append({
            "role": "user",
            "content": message,
            "timestamp": datetime.utcnow().isoformat()
        })

        full_response = ""
        async for chunk in self._runner.run(message):
            full_response += chunk
            yield chunk

        self.messages.append({
            "role": "assistant",
            "content": full_response,
            "timestamp": datetime.utcnow().isoformat()
        })

    async def cleanup(self):
        """Cleanup agent resources"""
        if self._mcp_tool:
            try:
                await self._mcp_tool.cleanup()
            except Exception as e:
                logger.warning(f"Error cleaning up MCP tool: {e}")
        self._agent = None
        self._thread = None
        self._runner = None


class BlinkitChaosAgentService:
    """
    Service to manage Blinkit Chaos Agent sessions
    """

    _sessions: Dict[str, BlinkitChaosAgentSession] = {}

    @classmethod
    async def create_session(cls, user_id: int) -> BlinkitChaosAgentSession:
        """Create a new chaos agent session"""
        import uuid
        session_id = f"chaos-{uuid.uuid4().hex[:12]}"

        session = BlinkitChaosAgentSession(session_id=session_id, user_id=user_id)
        await session.initialize()

        cls._sessions[session_id] = session
        logger.info(f"Created chaos agent session: {session_id}")

        return session

    @classmethod
    def get_session(cls, session_id: str) -> Optional[BlinkitChaosAgentSession]:
        """Get an existing session"""
        return cls._sessions.get(session_id)

    @classmethod
    def get_user_sessions(cls, user_id: int) -> list:
        """Get all sessions for a user"""
        return [s for s in cls._sessions.values() if s.user_id == user_id]

    @classmethod
    async def delete_session(cls, session_id: str) -> bool:
        """Delete a session"""
        session = cls._sessions.pop(session_id, None)
        if session:
            await session.cleanup()
            return True
        return False

    @classmethod
    async def chat(cls, session_id: str, message: str) -> AsyncGenerator[str, None]:
        """Send message to a session and stream response"""
        session = cls.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        async for chunk in session.chat(message):
            yield chunk

    @classmethod
    async def cleanup_all(cls):
        """Cleanup all sessions"""
        for session_id in list(cls._sessions.keys()):
            await cls.delete_session(session_id)
