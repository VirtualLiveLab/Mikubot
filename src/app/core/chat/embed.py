from typing import TYPE_CHECKING

from discord import Embed

from src.const.enums import Color

if TYPE_CHECKING:
    from .cog import OmikujiResult


def omikuji_embed(result: "OmikujiResult", description: str) -> Embed:
    return Embed(
        title="おみくじ",
        color=Color.MIKU,
        description=f"# {result}\n{description}",
    )
