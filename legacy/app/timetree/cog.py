import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands, tasks

from components.ui import StatusUI
from const.enums import Color, Status
from legacy.timetree import Client as TimeTreeClient
from utils.finder import Finder
from utils.time import TimeUtils

from .embed import today_event_embed

if TYPE_CHECKING:
    # import some original class
    from app.bot import Bot

    pass


class TimeTree(commands.Cog):
    def __init__(self, bot: "Bot") -> None:
        self.bot = bot
        self.send_today_event.start()

    async def cog_unload(self) -> None:
        self.send_today_event.cancel()

    @tasks.loop(seconds=60)
    async def send_today_event(self) -> None:
        if TimeUtils.get_now_jst().strftime("%H:%M") != "08:39":
            return
        embed = await self.get_timetree_embed()
        if embed is None:
            embed = discord.Embed(
                title="エラー",
                description="TimeTreeからの情報取得に失敗しました。",
                color=Color.WARNING,
            )

        channel = await Finder(self.bot).find_channel(int(os.environ["CHANNEL_ID"]), expected_type=discord.TextChannel)
        await channel.send(embed=embed)
        return

    @app_commands.guilds(int(os.environ["GUILD_ID"]))  # type: ignore[arg-type]
    @app_commands.command(name="timetree")
    async def send_timetree(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(thinking=False)

        ui = StatusUI(color=Color.MIKU)
        ui.add(
            key="TIMETREE",
            status=Status.IN_PROGRESS,
            message="TimeTreeから情報を取得しています...",
        )
        await ui.send(interaction.followup)

        embed = await self.get_timetree_embed()
        if embed is None:
            ui.update(
                key="TIMETREE",
                status=Status.FAILED,
                message="TimeTreeからの情報取得に失敗しました。",
            )
            ui.color = Color.WARNING
            await ui.sync()
            return

        ui.remove(key="TIMETREE")
        ui._dangerously_replace_embed(embed)  # noqa: SLF001
        await ui.sync()
        return

    async def get_timetree_embed(self) -> discord.Embed | None:
        client = TimeTreeClient(
            api_key=os.getenv("API_KEY", ""),
            calendar_id=os.getenv("CALENDAR_ID", ""),
        )
        try:
            events = await client.get_upcoming_events()
        except Exception:
            self.bot.logger.exception("TimeTreeからの情報取得に失敗しました")
            return None
        else:
            return today_event_embed(
                events=events,
                title="今日の予定",
                events_count=len(events),
            )


async def setup(bot: "Bot") -> None:
    await bot.add_cog(TimeTree(bot))
