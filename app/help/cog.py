from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands
from ductile.controller import InteractionController

from .const import FeatureLabel
from .view import HelpView

if TYPE_CHECKING:
    # import some original class
    from app.bot import Bot

    pass


class Help(commands.Cog):
    def __init__(self, bot: "Bot") -> None:
        self.bot = bot

    @app_commands.rename(feature_name="機能")  # type: ignore[arg-type]
    @app_commands.command(name="help", description="Botの使い方を表示するよ！")
    async def send_help_command(
        self,
        interaction: discord.Interaction,
        feature_name: FeatureLabel | None = None,
    ) -> None:
        await interaction.response.defer(ephemeral=True)
        if not feature_name:
            feature_name = "ヘルプ"
        controller = InteractionController(HelpView(command_name=feature_name), interaction=interaction)
        await controller.send()


async def setup(bot: "Bot") -> None:
    await bot.add_cog(Help(bot))
