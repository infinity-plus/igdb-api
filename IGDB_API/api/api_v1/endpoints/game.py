from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError

from IGDB_API.api.core.models import Game, GamePydantic
from IGDB_API.igdb import get_game_info

router = APIRouter()


class Status(BaseModel):
    message: str


@router.get(
    "/{game_name}",
    response_model=GamePydantic,
    responses={
        404: {"model": HTTPNotFoundError},
        500: {"model": Status},
        200: {"model": GamePydantic},
    },
)
async def get_game(game_name: str):
    game_obj = await Game.get_or_none(name__iexact=game_name)
    game_dict = game_obj.__dict__ if game_obj else {}
    game = (
        GamePydantic(
            **{
                k: v
                for k, v in game_dict.items()
                if k in GamePydantic.__fields__  # noqa: E501
            }
        )
        if game_dict
        else None
    )
    if not game:
        if game := await get_game_info(game_name):
            await Game.create(**game.dict())
        else:
            raise HTTPException(status_code=404, detail="Game not found")
    return game
