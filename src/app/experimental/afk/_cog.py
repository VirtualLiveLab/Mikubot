import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from src.components.status import StatusUI
from src.const.enums import Color, Status

if TYPE_CHECKING:
    # import some original class
    from src.app.bot import Bot

    pass


class AFK(commands.Cog):
    def __init__(self, bot: "Bot") -> None:
        self.bot = bot
        self.ctx_send_to_afk = app_commands.ContextMenu(
            name="すやすやすいみん",
            guild_ids=[int(os.environ["GUILD_ID"])],
            callback=self.ctx_send_to_afk_callback,
        )
        self.bot.tree.add_command(self.ctx_send_to_afk)

    async def ctx_send_to_afk_callback(self, interaction: discord.Interaction, member: discord.Member) -> None:
        await interaction.response.defer(ephemeral=True)

        ui = StatusUI(color=Color.MIKU, title="すやすや")
        if not member.voice:
            ui.add(
                key="SLP",
                status=Status.FAILED,
                message=f"{member.mention} さんはボイスチャンネルに接続していません。",
            )
            await ui.send(interaction.followup, ephemeral=True)
            return

        if not interaction.guild or not (afk := interaction.guild.afk_channel):
            ui.add(
                key="SLP",
                status=Status.FAILED,
                message=f"{member.mention} さんをすいみんチャンネルに転送できませんでした。",
            )
            await ui.send(interaction.followup, ephemeral=True)
            return

        ui.add(
            key="SLP",
            status=Status.IN_PROGRESS,
            message=f"{member.mention} さんをすいみんチャンネルに転送しています...",
        )
        await ui.send(interaction.followup, ephemeral=True)

        try:
            await member.move_to(afk)
        except discord.Forbidden:
            ui.update(
                key="SLP",
                status=Status.FAILED,
                message="権限がありません。",
            )
            await ui.sync()
        except discord.HTTPException:
            ui.update(
                key="SLP",
                status=Status.FAILED,
                message="操作に失敗しました。",
            )
            await ui.sync()
        except Exception:  # noqa: BLE001
            ui.update(
                key="SLP",
                status=Status.FAILED,
                message="不明なエラーが発生しました。",
            )
        else:
            ui.update(
                key="SLP",
                status=Status.SUCCESS,
                message=f"{member.mention} さんをすいみんチャンネルに転送しました。",
            )
            await ui.sync()
        return


async def setup(bot: "Bot") -> None:
    await bot.add_cog(AFK(bot))
