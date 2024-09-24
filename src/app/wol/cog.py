import os
from typing import TYPE_CHECKING

from discord import Embed, Interaction, app_commands
from discord.ext import commands
from ductile.controller import InteractionController

from .fn import get_computer_status
from .view import WOLView

if TYPE_CHECKING:
    # import some original class
    from src.app.bot import Bot


class WOL(commands.Cog):
    def __init__(self, bot: "Bot") -> None:
        self.bot = bot

    @app_commands.guild_only()
    @app_commands.command(name="wol", description="部室のPCを遠隔起動するよ！")
    async def wol(self, interaction: Interaction) -> None:
        await interaction.response.defer(ephemeral=True)

        cf_id = os.getenv("CF_ACCESS_CLIENT_ID")
        cf_secret = os.getenv("CF_ACCESS_CLIENT_SECRET")

        if cf_id is None or cf_secret is None:
            e = Embed(title="エラー", description="必要な値が設定されていないので使えないよ...")
            e.add_field(name="CF_ACCESS_CLIENT_ID", value="❌ 未設定" if cf_id is None else "✅ OK")
            e.add_field(name="CF_ACCESS_CLIENT_SECRET", value="❌ 未設定" if cf_secret is None else "✅ OK")

            await interaction.followup.send(embed=e, ephemeral=True)
            return

        current_status = await get_computer_status()
        view = WOLView(initial_status=current_status)
        controller = InteractionController(view, interaction=interaction, timeout=None, ephemeral=True)

        await controller.send()
        await controller.wait()


async def setup(bot: "Bot") -> None:
    await bot.add_cog(WOL(bot))
