import discord

from src.const.enums import Color


def user_embed(
    user: discord.Member | discord.User,
) -> discord.Embed:
    embed = discord.Embed(
        title=user.display_name,
        color=Color.MIKU,
    )
    embed.add_field(name="ユーザー名", value=user.display_name)
    embed.add_field(
        name="固有 ID",
        value=user.id,
    )
    embed.set_thumbnail(url=user.display_avatar.url)
    return embed
