from typing import List

from fastapi import APIRouter
from pydantic import BaseModel
from tortoise.exceptions import IncompleteInstanceError, IntegrityError

from IGDB_API.api.core.models import Game, GamePydantic
from IGDB_API.igdb import get_game_info

router = APIRouter()


class Status(BaseModel):
    message: str


@router.get(
    "/{game_name}",
    response_model=List[GamePydantic],
    responses={
        500: {"model": Status},
    },
)
async def get_game(game_name: str):
    ret_list = []
    if games := await Game.filter(name__icontains=game_name):
        for game_obj in games:
            game_dict = game_obj.__dict__ if game_obj else {}
            game = (
                GamePydantic(
                    **{
                        k: v
                        for k, v in game_dict.items()
                        if k in GamePydantic.__fields__
                    }
                )
                if game_dict
                else None
            )
            if game:
                ret_list.append(game)
    elif games := await get_game_info(game_name):
        for game in games:
            ret_list.append(game)
            try:
                await Game.create(**game.dict())
            except (IntegrityError, IncompleteInstanceError):
                pass
    return ret_list
