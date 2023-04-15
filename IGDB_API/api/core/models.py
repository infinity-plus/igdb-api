import re
from time import gmtime as current_time
from time import mktime as time_to_posix

from tortoise import fields
from tortoise.contrib.pydantic.creator import pydantic_model_creator
from tortoise.models import Model
from tortoise.validators import RegexValidator


class Game(Model):
    """Game model for storing game info"""

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="Name of the game")
    summary = fields.TextField(description="Summary of the game", null=True)

    cover_url = fields.CharField(
        max_length=255,
        description="Cover image url",
        validators=[
            RegexValidator(
                r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)",  # noqa: E501
                re.IGNORECASE,
            )
        ],
        default="https://via.placeholder.com/264x352",
    )


class Token(Model):
    """Token model for storing access token and expiry time"""

    id = fields.IntField(pk=True)
    access_token = fields.CharField(max_length=255)
    expires_in = fields.FloatField()
    #  time_stamp in posix time
    time_stamp = fields.DatetimeField(auto_now=True)

    def is_expired(self):
        """Check if token is expired"""
        return (
            time_to_posix(current_time())
            > self.time_stamp.timestamp() + self.expires_in
        )

    class Meta:
        """Meta class for Token model"""

        table = "token"


GamePydantic = pydantic_model_creator(Game, name="Game")
TokenPydantic = pydantic_model_creator(Token, name="Token")
