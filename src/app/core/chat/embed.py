from typing import TYPE_CHECKING

import discord
from discord import Embed

from src.const.enums import Color
from src.utils.time import TimeUtils

if TYPE_CHECKING:
    from .cog import OmikujiResult


def user_embed(
    user: discord.Member | discord.User,
) -> Embed:
    embed = Embed(
        title=user.display_name,
        color=Color.MIKU,
    )
    embed.add_field(
        name="Created at",
        value=TimeUtils.dt_to_str(user.created_at),
    )
    embed.add_field(
        name="ID",
        value=user.id,
    )
    embed.set_thumbnail(url=user.display_avatar.url)
    return embed


def omikuji_embed(result: "OmikujiResult", description: str) -> Embed:
    return Embed(
        title="おみくじ",
        color=Color.MIKU,
        description=f"# {result}\n{description}",
    )
