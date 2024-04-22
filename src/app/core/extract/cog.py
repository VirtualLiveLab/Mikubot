import os
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from src.packages.url_extractor import DiscordPlugin, NotionPlugin, UrlExtractor
from src.utils.logger import get_my_logger

from .embed import process_message_to_embeds, process_notion_page_to_embeds
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
                "notion": NotionPlugin(workspace=os.environ["NOTION_DOMAIN"]),
            }
        )
        matches = await url_extractor.find_all_async(message.content)
        self.__logger.debug("matches: %s", matches)

        if (d := matches["discord"]) is not None:
            self.__logger.debug("discord message url found: %s", d)
            extractor = DiscordProcessor(self.bot)
            extracted_messages = await extractor.from_matches_async(matches=d)

            for msg in extracted_messages:
                try:
                    await message.channel.send(
                        embeds=process_message_to_embeds(msg),
                        view=DispandView(
                            message_url=msg.jump_url,
                            button_label="元のメッセージを見る",
                        ),
                    )
                except Exception:
                    self.bot.logger.exception("dispand error: discord")
            return

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


async def setup(bot: "Bot") -> None:
    await bot.add_cog(Extract(bot))
