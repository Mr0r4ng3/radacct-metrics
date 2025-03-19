from fastapi.routing import APIRouter

from app.api.v1.routes import auth, radacct, users

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(radacct.router, prefix="/radacct", tags=["radacct"])
