import re
from time import gmtime as current_time
from time import mktime as time_to_posix

from tortoise import fields
from tortoise.contrib.pydantic.creator import pydantic_model_creator
from tortoise.models import Model
from tortoise.validators import RegexValidator


class Game(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="Name of the game")
    summary = fields.TextField(description="Summary of the game")

    cover_url = fields.CharField(
        max_length=255,
        description="Cover image url",
        validators=[
            RegexValidator(
                r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)",  # noqa: E501
                re.IGNORECASE,
            )
        ],
    )


#  class to store access token and expiry time
class Token(Model):
    id = fields.IntField(pk=True)
    access_token = fields.CharField(max_length=255)
    expires_in = fields.FloatField()
    #  time_stamp in posix time
    time_stamp = fields.DatetimeField(auto_now=True)

    #  method to check if the token is expired by comparing it with the
    # current time
    def is_expired(self):
        return (
            time_to_posix(current_time())
            > self.time_stamp.timestamp() + self.expires_in
        )

    class Meta:
        table = "token"


GamePydantic = pydantic_model_creator(Game, name="Game")
TokenPydantic = pydantic_model_creator(Token, name="Token")
