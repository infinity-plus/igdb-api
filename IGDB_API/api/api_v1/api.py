from fastapi import APIRouter

from .endpoints import game

router = APIRouter()
router.include_router(game.router, prefix="/game", tags=["Game"])
