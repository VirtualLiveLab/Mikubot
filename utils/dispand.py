import re
from typing import TypedDict

import discord
from discord import Client, Colour, Embed, Message

from const.discord import MAX_EMBEDS_PER_MESSAGE

regex_discord_message_url = (
    "(?!<)https://(ptb.|canary.)?discord(app)?.com/channels/"
    "(?P<guild>[0-9]{17,20})/(?P<channel>[0-9]{17,20})/(?P<message>[0-9]{17,20})(?!>)"
)
regex_extra_url = (
    r"\?base_aid=(?P<base_author_id>[0-9]{17,20})&aid=(?P<author_id>[0-9]{17,20})&extra=(?P<extra_messages>(|[0-9,]+))"
)


class ExtractedMessage(TypedDict):
    guild_id: int
    channel_or_thread_id: int
    message_id: int
    jump_url: str
    embeds: list[Embed]


class MessageDispander:
    def __init__(self, client: Client) -> None:
        self._client = client

    async def dispand(self, *, message: discord.Message) -> list[ExtractedMessage]:
        if not message.guild:
            return []
        # mock message
        return [
            {
                "channel_or_thread_id": message.channel.id,
                "guild_id": message.guild.id,
                "message_id": message.id,
                "jump_url": message.jump_url,
                "embeds": [compose_embed(message, with_reference=True, accent_color=True)],
            },
        ]


async def dispand(*, message: Message, with_reference: bool = True, accent_color: int = 0x3498DB) -> list[ExtractedMessage]:
    messages = await extract_message(message)
    extracted: list[ExtractedMessage] = []
    for msg in messages:
        embeds = []
        if msg.content or msg.attachments:
            embeds.append(compose_embed(msg, with_reference=with_reference, accent_color=accent_color))
        # Send the second and subsequent attachments with embed (named 'embed') respectively:
        for attachment in msg.attachments[1:]:
            embed = Embed()
            embed.set_image(url=attachment.proxy_url)
            embeds.append(embed)

        # add msg.embeds until embeds reaches 10
        for embed in msg.embeds:
            if len(embeds) >= MAX_EMBEDS_PER_MESSAGE:
                break
            embeds.append(embed)

        # extracted.append(
        #     {
        #         "id": msg.id,
        #         "jump_url": msg.jump_url,
        #         "embeds": embeds,
        #     },
        # )
    return extracted


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
