from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from utils.extract import MessageExtractor

from .embed import process_message_to_embeds, user_embed
from .view import DispandView

if TYPE_CHECKING:
    # import some original class
    from app.bot import Bot

    pass


class Chat(commands.Cog):
    def __init__(self, bot: "Bot") -> None:
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def add_reaction_to_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        match message.content:
            case "miku":
                await message.channel.send("MIKU!")
            case "ミクさん！":
                await message.channel.send("呼んだ？")
            case "うおうお":
                await message.add_reaction("\N{FISH}")
            case "ふろ":
                await message.add_reaction("\N{bathtub}")
            case "Docker":
                await message.add_reaction("\N{whale}")
            case _:
                pass

    @app_commands.command(name="miku", description="ミクさんが返事をしてくれるよ！")  # type: ignore[arg-type]
    async def call_miku(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send("MIKU!")

    @app_commands.command(name="helloworld", description="Hello World!")  # type: ignore[arg-type]
    async def hello_world(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=False)
        emb = user_embed(interaction.user)
        await interaction.followup.send(embed=emb)

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message) -> None:
        if message.author.id == self.bot.user.id:  # type: ignore[union-attr]
            return

        extractor = MessageExtractor(self.bot)
        extracted_messages = await extractor.extract_from_message(message=message)

        for msg in extracted_messages:
            try:
                await message.channel.send(
                    embeds=process_message_to_embeds(msg),
                    view=DispandView(message_url=msg.jump_url),
                )
            except Exception:
                self.bot.logger.exception("dispand error")
        return


async def setup(bot: "Bot") -> None:
    await bot.add_cog(Chat(bot))
