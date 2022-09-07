from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, covid, chest_abn

api_router = APIRouter()
api_router.include_router(chest_abn.router, prefix="/pred", tags=["Models"])
api_router.include_router(covid.router, prefix="/covid", tags=["Models"])
api_router.include_router(login.router, tags=["Users"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
