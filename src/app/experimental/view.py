import discord
from discord.app_commands import AppCommandChannel, AppCommandThread
from ductile import State, View, ViewObject
from ductile.ui import Button, ChannelSelect, MentionableSelect, Modal, Select, SelectOption, TextInput, UserSelect

from src.const.emoji import WASTE_BASKET


class TestView(View):
    def __init__(self) -> None:
        self.count = State(0, self)
        self.selected = State[list[str]]([], self)
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
                    },
                    style={
                        "placeholder": "Select",
                        "row": 1,
                    },
                    options=[
                        SelectOption(label="A", description="Aです"),
                        SelectOption(label="B", description="Bです"),
                    ],
                    on_select=on_select,
                ),
            ],
        )


class SelectView(View):
    def __init__(self) -> None:
        self.selected_channel = State[list[AppCommandChannel | AppCommandThread]]([], self)
        self.selected_user = State[list[discord.User | discord.Member]]([], self)
        self.selected_mentionable = State[list[discord.User | discord.Member | discord.Role]]([], self)
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
                    config={
                        "min_values": 1,
                        "max_values": 4,
                        "channel_types": [discord.ChannelType.text, discord.ChannelType.voice],
                    },
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
