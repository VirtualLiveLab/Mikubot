from typing import Annotated, ClassVar, Literal

from pydantic import UUID4, BaseModel, ConfigDict, Field
from pydantic_core import Url

__all__ = ["PersonUser", "BotUser"]

"""
User objects appear in the API in nearly all objects returned by the API, including:

Block object under created_by and last_edited_by.
Page object under created_by and last_edited_by and in people property items.
Database object under created_by and last_edited_by.
Rich text object, as user mentions.
Property object when the property is a people property.

User objects will always contain object and id keys, as described below.
The remaining properties may appear if the user is being rendered in a rich text or page property context,
and the bot has the correct capabilities to access those properties.
For more about capabilities, see the Capabilities guide and the Authorization guide.
"""


class BaseUser(BaseModel):
    object: Literal["user"]
    """
    Always `user`.
    """
    id: UUID4
    """
    Unique identifier for this user.
    """
    name: Annotated[str | None, Field(default_factory=lambda: None)]
    """
    User's name, as displayed in Notion.
    """
    avatar_url: Annotated[Url | None, Field(default_factory=lambda: None)]
    """
    Chosen avatar image.
    """

    model_config = {"frozen": True}


class PersonUserPerson(BaseModel):
    email: Annotated[str | None, Field(default_factory=lambda: None)]
    """
    Email address of person.
    This is only present if an integration has user capabilities that allow access to email addresses.
    """

    model_config = {"frozen": True}


class PersonUser(BaseUser):
    type: Annotated[Literal["person"] | None, Field(default_factory=lambda: None)]
    """
    Always `person`.
    """
    person: Annotated[PersonUserPerson | None, Field(default_factory=lambda: None)]
    """
    Additional information about the person.
    """

    model_config = {"frozen": True}


class BotUserBotOwnerWorkspace(BaseModel):
    type: Annotated[Literal["workspace"] | None, Field(default_factory=lambda: None)]
    """
    Always `workspace`.
    """
    workspace: Annotated[Literal[True] | None, Field(default_factory=lambda: None)]
    """
    Always `True`.
    """

    model_config: ClassVar[ConfigDict] = {"frozen": True}


class BotUserBotOwnerUser(BaseModel):
    type: Annotated[Literal["person"] | None, Field(default_factory=lambda: None)]
    """
    Always `person`.
    """
    user: Annotated[PersonUser | None, Field(default_factory=lambda: None)]
    """
    Information about the user.
    """

    model_config: ClassVar[ConfigDict] = {"frozen": True}


class BotUserBot(BaseModel):
    owner: Annotated[BotUserBotOwnerUser | BotUserBotOwnerWorkspace | None, Field(default_factory=lambda: None)]
    """
    Information about the owner of the bot.
    """

    model_config: ClassVar[ConfigDict] = {"frozen": True}


class BotUser(BaseUser):
    type: Annotated[Literal["bot"] | None, Field(default_factory=lambda: None)]
    """
    Always `bot`.
    """
    bot: Annotated[BotUserBot | None, Field(default_factory=lambda: None)]
    """
    Additional information about the bot.
    """

    model_config = {"frozen": True}
