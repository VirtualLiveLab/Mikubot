from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from src.packages.url_extracter import DiscordPlugin, NotionPlugin, UrlExtractor
from src.utils.extract import DiscordExtractor

from .embed import process_message_to_embeds
from .view import DispandView

if TYPE_CHECKING:
    # import some original class
    from src.app.bot import Bot


class Extract(commands.Cog):
    def __init__(self, bot: "Bot") -> None:
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message) -> None:
        if self.bot.user is not None and message.author.id == self.bot.user.id:
            return

        url_extractor = UrlExtractor({"discord": DiscordPlugin(), "notion": NotionPlugin(workspace="virtual-live-lab")})
        matches = await url_extractor.find_all_async(message.content)

        if (d := matches["discord"]) is not None:
            extractor = DiscordExtractor(self.bot)
            extracted_messages = await extractor.from_matches(matches=d)

            for msg in extracted_messages:
                try:
                    await message.channel.send(
                        embeds=process_message_to_embeds(msg),
                        view=DispandView(message_url=msg.jump_url),
                    )
                except Exception:
                    self.bot.logger.exception("dispand error")
            return

        if (n := matches["notion"]) is not None:  # noqa: F841
            pass


async def setup(bot: "Bot") -> None:
    await bot.add_cog(Extract(bot))
