from fastapi import APIRouter
from .gpt import router

api_router = APIRouter()
api_router.include_router(router, tags=["chatgpt"])
