from datetime import datetime
from typing import Literal

from pydantic import UUID4, BaseModel

from .parent import BlockParent, PageParent
from .user import BotUser, PersonUser


class Comment(BaseModel):
    object: Literal["comment"]
    """
    Always `comment`.
    """
    id: UUID4
    """
    Unique identifier for this comment.
    """
    parent: BlockParent | PageParent
    """
    Information about the comment's parent. See Parent object.
    Note that comments may only be parented by pages or blocks.
    """
    discussion_id: UUID4
    """
    Unique identifier of the discussion thread that the comment is associated with.
    """
    created_time: datetime
    """
    Date and time when this comment was created.
    Formatted as an ISO 8601 date time string.
    """
    last_edited_time: datetime
    """
    Date and time when this comment was updated.
    Formatted as an ISO 8601 date time string.Date and time when this comment was updated.
    Formatted as an ISO 8601 date time string.
    """
    created_by: PersonUser | BotUser
    """
    User who created the comment.
    """

    model_config = {"frozen": True}
