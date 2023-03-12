from typing import List

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
    response_model=List[GamePydantic],
    responses={
        404: {"model": HTTPNotFoundError},
        500: {"model": Status},
    },
)
async def get_game(game_name: str):
    games = await Game.filter(name__icontains=game_name)
    ret_list = []
    if games:
        for game_obj in games:
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
            if game:
                ret_list.append(game)
    if not games:
        if games := await get_game_info(game_name):
            for game in games:
                ret_list.append(game)
                try:
                    await Game.create(**game.dict())
                except Exception:
                    pass
        else:
            raise HTTPException(
                status_code=404,
                detail="Game not found",
            )
    return ret_list
