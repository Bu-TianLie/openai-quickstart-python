from fastapi import APIRouter
from .chatgpt import router

api_router = APIRouter()
api_router.include_router(router, tags=["chatgpt"])
