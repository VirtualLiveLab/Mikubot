import re

import discord
from discord import Client, Colour, Embed, Message

from .finder import Finder

regex_discord_message_url = (
    "(?!<)https://(ptb.|canary.)?discord(app)?.com/channels/"
    "(?P<guild>[0-9]{17,20})/(?P<channel>[0-9]{17,20})/(?P<message>[0-9]{17,20})(?!>)"
)
regex_extra_url = (
    r"\?base_aid=(?P<base_author_id>[0-9]{17,20})&aid=(?P<author_id>[0-9]{17,20})&extra=(?P<extra_messages>(|[0-9,]+))"
)


class MessageExtractor:
    def __init__(self, client: Client) -> None:
        self._client = client

    async def extract_from_message(self, *, message: discord.Message) -> list[Message]:
        if message.guild is None:
            return []

        # extract messages
        return await self._extract_from_message(message)

    async def _extract_from_message(self, message: Message) -> list[Message]:
        messages: list[Message] = []
        for ids in re.finditer(regex_discord_message_url, message.content):
            if message.guild is None:
                continue
            fetched_message = await self._fetch_message_from_id(
                guild_id=int(ids["guild"]),
                channel_id=int(ids["channel"]),
                message_id=int(ids["message"]),
            )
            if fetched_message is not None:
                messages.append(fetched_message)
        return messages

    async def _fetch_message_from_id(self, guild_id: int, channel_id: int, message_id: int) -> Message | None:
        finder = Finder(self._client)
        await finder.find_guild(guild_id)

        channel = await finder.find_channel(channel_id)
        if not isinstance(channel, discord.TextChannel | discord.VoiceChannel | discord.Thread):
            return None

        try:
            return await channel.fetch_message(message_id)
        except Exception:  # noqa: BLE001
            return None


# async def dispand(*, message: Message, with_reference: bool = True, accent_color: int = 0x3498DB):
#     messages = await extract_message(message)
#     extracted: list[ExtractedMessage] = []
#     for msg in messages:
#         embeds = []
#         if msg.content or msg.attachments:
#             embeds.append(compose_embed(msg, with_reference=with_reference, accent_color=accent_color))
#         # Send the second and subsequent attachments with embed (named 'embed') respectively:
#         for attachment in msg.attachments[1:]:
#             embed = Embed()
#             embed.set_image(url=attachment.proxy_url)
#             embeds.append(embed)

#         # add msg.embeds until embeds reaches 10
#         for embed in msg.embeds:
#             if len(embeds) >= MAX_EMBEDS_PER_MESSAGE:
#                 break
#             embeds.append(embed)

#         # extracted.append(
#         #     {
#         #         "id": msg.id,
#         #         "jump_url": msg.jump_url,
#         #         "embeds": embeds,
#         #     },
#         # )
#     return extracted


async def extract_message(message: Message) -> list[Message]:
    messages = []
    for ids in re.finditer(regex_discord_message_url, message.content):
        if message.guild is None:
            continue
        if message.guild.id != int(ids["guild"]):
            continue
        fetched_message = await fetch_message_from_id(
            guild=message.guild,
            channel_id=int(ids["channel"]),
            message_id=int(ids["message"]),
        )
        messages.append(fetched_message)
    return messages


async def fetch_message_from_id(guild: discord.Guild, channel_id: int, message_id: int) -> Message:
    channel = guild.get_channel_or_thread(channel_id)
    if channel is None:
        channel = await guild.fetch_channel(channel_id)
    # TODO @sushi-chaaaan: fix handling of ForumChannel and CategoryChannel  # noqa: TD003, FIX002
    if isinstance(channel, discord.ForumChannel | discord.CategoryChannel):
        raise NotImplementedError
    return await channel.fetch_message(message_id)


def compose_embed(message: Message, *, with_reference: bool, accent_color: int = 0x3498DB) -> Embed:
    if isinstance(message.channel, discord.DMChannel | discord.PartialMessageable | discord.GroupChannel):
        raise NotImplementedError
    embed = Embed(
        description=message.content,
        color=Colour(accent_color),
        timestamp=message.created_at,
    )
    embed.set_author(
        name=message.author.display_name,
        icon_url=message.author.display_avatar or f"{discord.Asset.BASE}/embed/avatars/{discord.DefaultAvatar.red}.png",
    )
    embed.add_field(
        name="送信した人",
        value=message.author.mention,
    )
    embed.add_field(
        name="チャンネル",
        value=message.channel.mention or "",
    )
    if with_reference:
        embed.add_field(
            name="元のメッセージ",
            value=f"[移動]({message.jump_url})",
        )
    if message.attachments and message.attachments[0].proxy_url:
        embed.set_image(url=message.attachments[0].proxy_url)
    return embed
