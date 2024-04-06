from typing import Literal

from pydantic import UUID4, BaseModel

"""
Pages, databases, and blocks are either located inside other pages, databases, and blocks,
or are located at the top level of a workspace. This location is known as the "parent".
Parent information is represented by a consistent parent object throughout the API.

General parenting rules:

- Pages can be parented by other pages, databases, blocks, or by the whole workspace.
- Blocks can be parented by pages, databases, or blocks.
- Databases can be parented by pages, blocks, or by the whole workspace.
"""


class DataBaseParent(BaseModel):
    type: Literal["database_id"]
    """
    Always `database_id`.
    """
    database_id: UUID4
    """
    The ID of the database that this page belongs to.
    """

    model_config = {"frozen": True}


class PageParent(BaseModel):
    type: Literal["page_id"]
    """
    Always `page_id`.
    """
    page_id: UUID4
    """
    The ID of the page that this page belongs to.
    """

    model_config = {"frozen": True}


class WorkspaceParent(BaseModel):
    """
    A page with a workspace parent is a top-level page within a Notion workspace.
    """

    type: Literal["workspace"]
    """
    Always `workspace`.
    """
    workspace: Literal[True]
    """
    Always `True`.
    """

    model_config = {"frozen": True}


class BlockParent(BaseModel):
    """
    A page may have a block parent if it is created inline in a chunk of text,

    or is located beneath another block like a toggle or bullet block.
    """

    type: Literal["block_id"]
    """
    Always `block_id`.
    """
    block_id: UUID4
    """
    The ID of the page that this page belongs to.
    """

    model_config = {"frozen": True}
