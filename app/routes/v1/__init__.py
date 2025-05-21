from fastapi import APIRouter, Depends, HTTPException

from app.routes.v1.user import r as user_router


router = APIRouter(
    prefix="/v1",
    tags=["v1"]
)
router.include_router(user_router)
