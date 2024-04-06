from datetime import datetime
from typing import Annotated, Literal, TypeAlias

from pydantic import UUID4, BaseModel, Field

from .parent import BlockParent, DataBaseParent, PageParent
from .user import BotUser, PersonUser

BlockType: TypeAlias = Literal[
    "bookmark",
    "breadcrumb",
    "bulleted_list_item",
    "callout",
    "child_database",
    "child_page",
    "column",
    "column_list",
    "divider",
    "embed",
    "equation",
    "file",
    "heading_1",
    "heading_2",
    "heading_3",
    "image",
    "link_preview",
    "link_to_page",
    "numbered_list_item",
    "paragraph",
    "pdf",
    "quote",
    "synced_block",
    "table",
    "table_of_contents",
    "table_row",
    "template",
    "to_do",
    "toggle",
    "unsupported",
    "video",
]


class Block(BaseModel):
    object: Literal["block"]
    """
    Always `block`.
    """
    id: UUID4
    """
    Identifier for this block.
    """
    parent: Annotated[PageParent | DataBaseParent | BlockParent | None, Field(default_factory=lambda: None)]
    """
    Information about the block's parent. See Parent object.
    """
    type: Annotated[BlockType | None, Field(default_factory=lambda: None)]
    """
    Type of block.
    """
    created_time: Annotated[datetime | None, Field(default_factory=lambda: None)]
    """
    Date and time when this block was created. Formatted as an ISO 8601 date time string.
    """
    created_by: Annotated[PersonUser | BotUser | None, Field(default_factory=lambda: None)]
    """
    User who created the block.
    """
    last_edited_time: Annotated[datetime | None, Field(default_factory=lambda: None)]
    """
    Date and time when this block was last updated. Formatted as an ISO 8601 date time string.
    """
    last_edited_by: Annotated[PersonUser | BotUser | None, Field(default_factory=lambda: None)]
    """
    User who last updated the block.
    """
    archived: Annotated[bool | None, Field(default_factory=lambda: None)]
    """
    The archived status of the block.
    """
    has_children: Annotated[bool | None, Field(default_factory=lambda: None)]
    """
    Whether or not the block has children blocks nested within it.
    """
