from fastapi import APIRouter
from app.api.routes import auth, users, friends, persona, gifts, social, agent

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(friends.router, prefix="/friends", tags=["Friends"])
api_router.include_router(persona.router, prefix="/persona", tags=["Persona"])
api_router.include_router(gifts.router, prefix="/gifts", tags=["Gifts"])
api_router.include_router(social.router, prefix="/social", tags=["Social Connections"])
api_router.include_router(agent.router, prefix="/agent", tags=["Chaos Agent"])
