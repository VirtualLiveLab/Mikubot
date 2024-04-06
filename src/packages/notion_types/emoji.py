from typing import Literal

from pydantic import BaseModel


class Emoji(BaseModel):
    """
    An emoji object contains information about an emoji character.
    It is most often used to represent an emoji that is rendered as a page icon in the Notion UI.
    """

    type: Literal["emoji"]
    """
    The constant string `emoji` that represents the object type.
    """
    emoji: str
    """
    The emoji character.
    """

    model_config = {"frozen": True}
