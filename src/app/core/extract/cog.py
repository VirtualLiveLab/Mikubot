import os
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from src.packages.url_extractor import DiscordPlugin, NotionPlugin, UrlExtractor
from src.utils.finder import Finder
from src.utils.logger import get_my_logger

from .embed import process_notion_page_to_embeds
from .processor import DiscordProcessor, NotionProcessor
from .view import DispandView

if TYPE_CHECKING:
    # import some original class
    from src.app.bot import Bot


class Extract(commands.Cog):
    def __init__(self, bot: "Bot") -> None:
        self.bot = bot
        self.__logger = get_my_logger(self.__class__.__name__)

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message) -> None:
        if self.bot.user is not None and message.author.id == self.bot.user.id:
            return

        url_extractor = UrlExtractor(
            {
                "discord": DiscordPlugin(),
                "notion": NotionPlugin(workspace=os.getenv("NOTION_DOMAIN") or ""),
            }
        )
        matches = await url_extractor.find_all_async(message.content)
        self.__logger.debug("matches: %s", matches)

        if (d := matches["discord"]) is not None:
            self.__logger.debug("discord message url found: %s", d)
            extractor = DiscordProcessor(self.bot)
            discord_messages = await extractor.from_matches_async(matches=d)

            for msg in discord_messages:
                try:
                    forwarded = await msg.forward(message.channel, fail_if_not_exists=False)
                    await forwarded.add_reaction("🗑️")
                except Exception:
                    self.bot.logger.exception("dispand error: discord")

        if (n := matches["notion"]) is not None:
            self.__logger.debug("notion url found: %s", n)
            extractor = NotionProcessor()
            extracted_messages = await extractor.from_matches_async(matches=n)
            for page in extracted_messages:
                try:
                    await message.channel.send(
                        embed=process_notion_page_to_embeds(page),
                        view=DispandView(message_url=page["url"], button_label="Notionを開く"),
                    )
                except Exception:
                    self.bot.logger.exception("dispand error: notion")

    @commands.Cog.listener("on_raw_reaction_add")
    async def cleanup_forwarded_messages(self, payload: discord.RawReactionActionEvent) -> None:
        if not self.bot.user or (bot_user_id := self.bot.user.id) is None:
            return

        # 自身によるリアクションは無視するべき
        # なぜなら、メッセージ転送後に自分て追加したリアクションで転送メッセージを消してしまうため
        if payload.user_id == bot_user_id:
            return

        is_correct_emoji = payload.emoji.name is not None and payload.emoji.name == "🗑️"
        # 自身が転送したメッセージ宛でないなら無視したい
        is_reaction_for_me = payload.message_author_id is not None and payload.message_author_id == bot_user_id

        if not is_correct_emoji or not is_reaction_for_me:
            return

        finder = Finder(self.bot)
        channel = await finder.find_channel(payload.channel_id)

        if not isinstance(channel, discord.TextChannel | discord.VoiceChannel | discord.StageChannel | discord.Thread):
            return

        message = await channel.fetch_message(payload.message_id)

        # 自身が転送したメッセージのうち MessageSnapShot があるものは確実に削除対象
        if message.message_snapshots == []:
            return

        await message.delete()


async def setup(bot: "Bot") -> None:
    await bot.add_cog(Extract(bot))
