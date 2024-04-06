from datetime import datetime
from typing import Literal

from pydantic import BaseModel
from pydantic_core import Url


class NotionHostedFileFile(BaseModel):
    url: Url
    """
    An authenticated S3 URL to the file.

    The URL is valid for one hour. If the link expires, then you can send an API request to get an updated URL.
    """
    expiry_time: datetime
    """
    The date and time when the link expires, formatted as an ISO 8601 date time string.
    """

    model_config = {"frozen": True}


class NotionHostedFile(BaseModel):
    type: Literal["file"]
    file: NotionHostedFileFile

    model_config = {"frozen": True}


class ExternalFileExternal(BaseModel):
    url: Url
    """
    The URL to the file.
    """

    model_config = {"frozen": True}


class ExternalFile(BaseModel):
    type: Literal["external"]
    external: ExternalFileExternal

    model_config = {"frozen": True}
