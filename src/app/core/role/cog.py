from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands
from ductile.controller import InteractionController

from .view import RoleCheckView

if TYPE_CHECKING:
    # import some original class
    from src.app.bot import Bot


class Role(commands.Cog):
    role = app_commands.Group(name="role", description="ロール関連のコマンド")

    def __init__(self, bot: "Bot") -> None:
        self.bot = bot

    @role.command(name="check", description="ロールを確認します。")
    async def check_role(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        controller = InteractionController(
            RoleCheckView(),
            interaction=interaction,
            timeout=None,
            ephemeral=True,
        )
        await controller.send()


async def setup(bot: "Bot") -> None:
    await bot.add_cog(Role(bot))
