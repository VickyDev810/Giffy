"""
Giftify Backend API
A social gifting platform for sending surprise gifts to friends
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import api_router
from app.core.database import Base, engine
from app.services.scheduler import start_scheduler, stop_scheduler
from app.services.blinkit_chaos_agent import BlinkitChaosAgentService
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting Giffy API...")

    # Create database tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")

    # Start gift scheduler
    await start_scheduler()
    logger.info("Gift scheduler started")

    yield

    # Shutdown
    logger.info("Shutting down Giffy API...")
    stop_scheduler()
    await BlinkitChaosAgentService.cleanup_all()
    logger.info("Chaos agent sessions cleaned up")


# Create FastAPI app
app = FastAPI(
    title="Giffy API",
    description="""
    ## Social Gifting Platform API

    Send surprise gifts to your friends with AI-powered gift selection!

    ### Features:
    - **Authentication**: JWT-based auth with signup/login
    - **Friends**: Send/accept friend requests, manage friendships
    - **Persona**: Create profiles with vibe tags, interests, and preferences
    - **Gifts**: Send one-time or recurring gifts with AI selection
    - **Social**: Connect Instagram for better gift recommendations
    - **Agents**: Integration with Blinkit, Zepto, Swiggy, Amazon
    - **Chaos Agent**: Real-time chat with AI agent for chaotic gift procurement via Blinkit

    ### Gift Flow:
    1. Select a friend
    2. Set budget and vibe prompt ("send something chaotic")
    3. AI agent picks the perfect gift
    4. Review and approve (or YOLO mode - auto-send!)
    5. Gift delivered via quick commerce
    """,
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Giffy API! 🎁",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "giftify-api",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
