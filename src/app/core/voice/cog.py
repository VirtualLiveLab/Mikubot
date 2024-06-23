import math
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands
from ductile.controller import InteractionController

from src.const.enums import TaskStatus

from .view import MaximizeBitrateView

if TYPE_CHECKING:
    # import some original class
    from src.app.bot import Bot


class Voice(commands.Cog):
    voice_group = app_commands.Group(name="voice", description="ボイスチャット関連のコマンド")

    def __init__(self, bot: "Bot") -> None:
        self.bot = bot

    @voice_group.command(name="maximize-bitrate", description="全ボイスチャットのビットレートを最大にします。")
    @app_commands.guild_only()
    async def maximize_bitrate(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        if (guild := interaction.guild) is None:
            await interaction.followup.send("このコマンドはサーバー内でのみ使用できます。", ephemeral=True)
            return

        view = MaximizeBitrateView(guild.voice_channels)
        controller = InteractionController(view, interaction=interaction, sync_interval=1)
        await controller.send()

        for channel in guild.voice_channels:
            try:
                await channel.edit(bitrate=math.floor(guild.bitrate_limit))
                view.set_task_state(channel.id, TaskStatus.SUCCESS)
            except Exception:
                msg = f"Failed to maximize bitrate in {channel.name}"
                self.bot.logger.exception(msg)
                view.set_task_state(channel.id, TaskStatus.ERROR)

        controller.stop()  # stop controller and execute last sync
        return


async def setup(bot: "Bot") -> None:
    await bot.add_cog(Voice(bot))
