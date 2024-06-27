from datetime import UTC, datetime

import discord

from src.const.discord import MAX_EMBEDS_PER_MESSAGE
from src.const.enums import Color
from src.utils.time import JST
from src.utils.timestamp import DiscordTimestamp, DiscordTimestampStyle

from .processor import NotionPage


def get_information_embed(message: discord.Message, color: int = Color.MIKU) -> discord.Embed:
    embed = discord.Embed(
        description=message.content,
        color=color,
        timestamp=message.created_at,
    )
    embed.set_author(
        name=message.author.display_name,
        icon_url=message.author.display_avatar.url or message.author.default_avatar.url,
    )
    embed.add_field(
        name="送信した人",
        value=message.author.mention,
    )
    if not isinstance(
        message.channel,
        discord.DMChannel | discord.PartialMessageable | discord.GroupChannel,
    ):
        embed.add_field(
            name="チャンネル",
            value=message.channel.mention or "",
        )
    if message.reference is not None:
        embed.add_field(
            name="返信先のメッセージ",
            value=message.reference.jump_url,
        )
    if message.attachments and message.attachments[0].url:
        embed.set_image(url=message.attachments[0].url)
    if message.guild is not None:
        embed.set_footer(text=f"Sent in {message.guild.name}")

    return embed


def get_poll_embed(poll: discord.Poll, color: int = Color.MIKU) -> discord.Embed:
    embed = discord.Embed(
        title="このメッセージには投票が含まれています。",
        color=color,
    )

    embed.add_field(
        name="質問",
        value=poll.question,
    )
    embed.add_field(
        name="現在の投票数",
        value=f"{poll.total_votes}票",
    )
    # 今は常に期限が存在するが、将来的に無期限の投票が追加される可能性がある
    # https://discord.com/developers/docs/resources/poll#poll-object
    if (exp := poll.expires_at) is not None:
        exp_jst = exp.astimezone(JST())
        now_jst = datetime.now(JST())
        time_left = exp_jst - now_jst

        if time_left.total_seconds() <= 0:  # 投票期限を過ぎている
            embed.add_field(
                name="終了済み",
                value="投票期限を過ぎています。",
                inline=False,
            )
        elif exp_jst.day == now_jst.day:  # 日本時間で今日中に終了する場合、相対残り時間で表示する
            embed.add_field(
                name="投票締め切りまで",
                value=DiscordTimestamp.from_datetime(exp, tz=UTC).export_with_style(DiscordTimestampStyle.RELATIVE),
                inline=False,
            )
        else:  # それ以外の場合、通常の日時で表示する
            embed.add_field(
                name="投票締め切りまで",
                value=DiscordTimestamp.from_datetime(exp, tz=UTC).export_with_style(
                    DiscordTimestampStyle.LONG_DATE_WITH_SHORT_TIME
                ),
                inline=False,
            )

    return embed


def process_message_to_embeds(message: discord.Message, color: int = Color.MIKU) -> list[discord.Embed]:
    embeds: list[discord.Embed] = []

    embeds.append(get_information_embed(message, color))

    if (p := message.poll) is not None:
        embeds.append(get_poll_embed(p, color))

    for attachment in message.attachments[1:]:
        if len(embeds) >= MAX_EMBEDS_PER_MESSAGE:
            break
        embeds.append(
            discord.Embed(
                color=color,
            ).set_image(url=attachment.url)
        )

    for _e in message.embeds:
        if len(embeds) >= MAX_EMBEDS_PER_MESSAGE:
            break
        embeds.append(_e)

    return embeds


def process_notion_page_to_embeds(page: NotionPage) -> discord.Embed:  #
    e = discord.Embed(
        title=f"{page['emoji']} {page['title']}" if page["emoji"] else page["title"],
        url=page["url"],
        color=Color.MIKU,
        timestamp=page["last_updated"],
    )
    e.set_image(url=page["image"])
    e.set_footer(text="Created on Notion")
    return e
