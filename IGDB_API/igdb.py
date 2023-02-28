from os import getenv
from typing import Optional

from requests import HTTPError, post

from IGDB_API import CLIENT_ID, CLIENT_SECRET
from IGDB_API.api.core.models import GamePydantic, Token, TokenPydantic


AUTH_URL = "https://id.twitch.tv/oauth2/token"
API_URL = "https://api.igdb.com/v4/games/"


class IGDBApiError(Exception):
    """Custom exception for IGDB API errors"""

    pass


async def get_access_token(client_id: str, client_secret: str) -> str:
    #  get token from database and check it is not expired
    token_obj = await Token.get_or_none()
    if token_obj and not token_obj.is_expired():
        return token_obj.access_token

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }
    try:
        response = post(AUTH_URL, headers=headers, data=data)
        response.raise_for_status()
        # Create Pydantic Object from API response
        print(response.json())
        token_obj = Token(**response.json())
        await token_obj.save()
    except HTTPError as e:
        raise IGDBApiError(f"Error getting access token: {e}") from e
    return token_obj.access_token


async def get_game_info(game: str) -> Optional["GamePydantic"]:  # type: ignore
    try:
        if CLIENT_SECRET is None or CLIENT_ID is None:
            raise ValueError(
                "CLIENT_ID or CLIENT_SECRET env variables invalid",
            )
        access_token = await get_access_token(CLIENT_ID, CLIENT_SECRET)
    except IGDBApiError as e:
        raise IGDBApiError(f"Error getting access token: {e}") from e

    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }
    request_params = {
        "headers": headers,
        "data": f'fields name,summary,cover.url; search "{game}"; limit 1;',
    }
    try:
        response = post(API_URL, **request_params)
        response.raise_for_status()

        # Create Pydantic Object from API response
        temp = response.json()[0]
        temp["cover_url"] = (
            temp.pop("cover")["url"]
            .replace("t_thumb", "t_cover_big")
            .replace("//", "https://")
        )
        game_obj = GamePydantic(**temp)
    except HTTPError as e:
        print(f"CLIENT_ID: {CLIENT_ID}")
        print(f"CLIENT_SECRET: {CLIENT_SECRET}")
        print(f"access_token: {access_token}")
        raise IGDBApiError(f"Error getting game info: {e}") from e
    return game_obj
