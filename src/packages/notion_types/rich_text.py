from typing import Annotated, Literal

from pydantic import BaseModel, Field
from pydantic_core import Url

from .color import NotionColor


class RichTextAnnotations(BaseModel):
    bold: bool
    """
    Whether the text is bolded.
    """
    italic: bool
    """
    Whether the text is italicized.
    """
    strikethrough: bool
    """
    Whether the text is struck through.
    """
    underline: bool
    """
    Whether the text is underlined.
    """
    code: bool
    """
    Whether the text is `code style`.
    """
    color: NotionColor
    """
    Color of the text.
    """


class RichTextObject(BaseModel):
    plain_text: str
    """
    The plain text without annotations.
    """
    annotations: RichTextAnnotations
    """
    The information used to style the rich text object.
    Refer to the annotation object section below for details.
    """
    href: Annotated[Url | None, Field(default_factory=lambda: None)]
    """
    The URL of any link or Notion mention in this text, if any.
    """


class Expression(RichTextObject):
    type: Literal["equation"]
    expression: str
    """
    The LaTeX string representing the inline equation.
    """


class MentionMention(BaseModel):
    type: Literal[
        "database",
        "date",
        "link_preview",
        "page",
        "template_mention",
        "user",
    ]
    """
    The type of the inline mention.
    """


class Mention(RichTextObject):
    type: Literal["mention"]
