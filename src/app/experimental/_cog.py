import asyncio
import os
from typing import TYPE_CHECKING, Literal

import discord
from discord import app_commands
from discord.ext import commands
from ductile.controller import InteractionController

from src.components.confirm_ui import ConfirmUI
from src.components.status import StatusUI
from src.const.enums import Color, Status

from .view import SelectView, TestView

if TYPE_CHECKING:
    # import some original class
    from src.app.bot import Bot


class TestCog(commands.Cog):
    def __init__(self, bot: "Bot") -> None:
        self.bot = bot

    @app_commands.guilds(int(os.environ["GUILD_ID"]))  # type: ignore[arg-type]
    @app_commands.command(name="experimental", description="実験的機能を試すコマンド")
    async def experimental(self, interaction: discord.Interaction, feature: Literal["status", "state", "select"]) -> None:
        if feature == "state":
            await self.try_state(interaction)
        elif feature == "status":
            await self.try_status(interaction)
        elif feature == "select":
            await self.try_select(interaction)
        else:
            await interaction.response.send_message("不明な機能です", ephemeral=True)

    async def try_status(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()

        ui = StatusUI(color=Color.MIKU)
        ui.add(key="STATUS_1", message="ステータス1")
        ui.add(key="STATUS_2", message="ステータス2")

        # msg = await interaction.followup.send(embed=status.to_embed(), wait=True)
        # status.set_message(msg)
        await ui.send(interaction.followup, ephemeral=False)
        ui.update(
            key="STATUS_1",
            status=Status.IN_PROGRESS,
            message="ステータス1を実行中",
        )
        await ui.sync()
        # await msg.edit(embed=status.to_embed())

        await asyncio.sleep(5)
        ui.update(key="STATUS_1", status=Status.SUCCESS, message="ステータス1を完了")
        ui.update(key="STATUS_2", status=Status.IN_PROGRESS, message="ステータス2を実行中")
        await ui.sync()

        await asyncio.sleep(5)
        ui.update(key="STATUS_2", status=Status.FAILED, message="ステータス2でエラーが発生")
        await ui.sync()

    async def try_state(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        controller = InteractionController(TestView(), interaction=interaction)
        await controller.send()

        res = await controller.wait()
        for k, v in res.states.items():
            await interaction.followup.send(f"State {k}: {v}")

    async def try_select(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()

        confirm_ui = ConfirmUI(title="テスト", description="続けますか?", default_result=False)
        res = await confirm_ui.send_and_wait(interaction)
        if not res:
            await interaction.followup.send("キャンセルしました", ephemeral=True)
            return

        controller = InteractionController(SelectView(), interaction=interaction)
        await controller.send()


async def setup(bot: "Bot") -> None:
    await bot.add_cog(TestCog(bot))
