import asyncio
import os
from typing import TYPE_CHECKING, Literal

import discord
from discord import ChannelType, app_commands
from discord.app_commands import AppCommandChannel, AppCommandThread
from discord.ext import commands

from components.ui import (
    Button,
    ChannelSelect,
    InteractionController,
    MentionableSelect,
    Modal,
    Select,
    SelectOption,
    State,
    StatusUI,
    TextInput,
    UserSelect,
    View,
    ViewObject,
)
from const.emoji import WASTE_BASKET
from const.enums import Color, Status

if TYPE_CHECKING:
    # import some original class
    from app.bot import Bot

    pass


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
        controller = InteractionController(SelectView(), interaction=interaction)
        await controller.send()


class TestView(View):
    def __init__(self) -> None:
        self.count = State(0, self)
        self.selected: State[list[str]] = State([], self)
        super().__init__()

    def render(self) -> ViewObject:
        async def increment(interaction: discord.Interaction) -> None:
            await interaction.response.defer()
            self.count.set_state(lambda x: x + 1)

        async def decrement(interaction: discord.Interaction) -> None:
            await interaction.response.defer()
            self.count.set_state(lambda x: x - 1)

        async def on_submit(interaction: discord.Interaction, values: dict[str, str]) -> None:
            await interaction.response.defer(ephemeral=True)
            try:
                value = int(values["数字"])
            except ValueError:
                return await interaction.followup.send("数字を入力してください", ephemeral=True)
            else:
                self.count.set_state(value)

        async def send_modal(interaction: discord.Interaction) -> None:
            await interaction.response.send_modal(
                Modal(
                    title="数字を入力してください",
                    inputs=[
                        TextInput(
                            "数字",
                            style={
                                "default": str(self.count.get_state()),
                                "placeholder": "数字を入力してください",
                                "row": 0,
                                "field": "short",
                            },
                            config={"required": True, "min_length": 1, "max_length": 3},
                        ),
                    ],
                    on_submit=on_submit,
                ),
            )

        async def reset(interaction: discord.Interaction) -> None:
            await interaction.response.defer()
            self.count.set_state(0)

        async def stop(interaction: discord.Interaction) -> None:
            await interaction.response.defer()
            self.stop()

        async def on_select(interaction: discord.Interaction, values: list[str]) -> None:
            await interaction.response.defer()
            self.selected.set_state(values)

        e = discord.Embed(
            title="Count",
            description=f"Count: {self.count.get_state()}",
        )
        e.add_field(name="Selected", value="\n".join(self.selected.get_state()))

        return ViewObject(
            embeds=[e],
            components=[
                Button("+1", style={"color": "green"}, on_click=increment),
                Button("-1", style={"color": "red"}, on_click=decrement),
                Button("input", style={"color": "blurple"}, on_click=send_modal),
                Button(
                    "Reset",
                    style={
                        "color": "blurple",
                        "emoji": "🔄",
                        "disabled": self.count.get_state() == 0,
                    },
                    on_click=reset,
                ),
                Button(style={"emoji": WASTE_BASKET, "color": "red"}, on_click=stop),
                Select(
                    config={
                        "max_values": 2,
                        "options": [
                            SelectOption(label="A", description="Aです"),
                            SelectOption(label="B", description="Bです"),
                        ],
                    },
                    style={
                        "placeholder": "Select",
                        "row": 1,
                    },
                    on_select=on_select,
                ),
            ],
        )


class SelectView(View):
    def __init__(self) -> None:
        self.selected_channel: State[list[AppCommandChannel | AppCommandThread]] = State([], self)
        self.selected_user: State[list[discord.User | discord.Member]] = State([], self)
        self.selected_mentionable: State[list[discord.User | discord.Member | discord.Role]] = State([], self)
        super().__init__()

    def render(self) -> ViewObject:
        e = discord.Embed(
            title="Select",
        )
        e.add_field(name="Selected Channel", value="\n".join(s.name for s in self.selected_channel.get_state()))
        e.add_field(name="Selected User", value="\n".join(s.name for s in self.selected_user.get_state()))
        e.add_field(name="Selected Mentionable", value="\n".join(s.name for s in self.selected_mentionable.get_state()))

        async def on_channel_select(
            interaction: discord.Interaction,
            values: list[AppCommandChannel | AppCommandThread],
        ) -> None:
            await interaction.response.defer()
            self.selected_channel.set_state(values)

        async def on_user_select(interaction: discord.Interaction, values: list[discord.User | discord.Member]) -> None:
            await interaction.response.defer()
            self.selected_user.set_state(values)

        async def on_mentionable_select(
            interaction: discord.Interaction,
            values: list[discord.User | discord.Member | discord.Role],
        ) -> None:
            await interaction.response.defer()
            self.selected_mentionable.set_state(values)

        return ViewObject(
            embeds=[e],
            components=[
                ChannelSelect(
                    config={"min_values": 1, "max_values": 4, "channel_types": [ChannelType.text, ChannelType.voice]},
                    style={"placeholder": "select channel", "row": 0},
                    on_select=on_channel_select,
                ),
                UserSelect(
                    config={"min_values": 1, "max_values": 4},
                    style={"placeholder": "select user", "row": 1},
                    on_select=on_user_select,
                ),
                MentionableSelect(
                    config={"min_values": 1, "max_values": 4},
                    style={"placeholder": "select mentionable", "row": 2},
                    on_select=on_mentionable_select,
                ),
            ],
        )


async def setup(bot: "Bot") -> None:
    await bot.add_cog(TestCog(bot))
