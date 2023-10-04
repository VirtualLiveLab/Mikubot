import discord
from ductile import State, View, ViewObject
from ductile.ui import Select, SelectOption

from .const import FEATURE_LABEL_LIST, FeatureLabel
from .embed import get_help_embed


class HelpView(View):
    def __init__(self, command_name: FeatureLabel) -> None:
        super().__init__()
        self.current = State[FeatureLabel](command_name, self)

    def render(self) -> ViewObject:
        async def on_select(interaction: discord.Interaction, values: list[str]) -> None:
            await interaction.response.defer(ephemeral=True)
            if (selected := values[0]) not in FEATURE_LABEL_LIST:
                selected = "ヘルプ"
            self.current.set_state(selected)

        return ViewObject(
            embeds=[
                get_help_embed(self.current()),
            ],
            components=[
                Select(
                    config={
                        "max_values": 1,
                    },
                    style={
                        "placeholder": "使い方を見たい機能を選択してください。",
                    },
                    options=[
                        SelectOption(label=n, value=n, selected_by_default=n == self.current()) for n in FEATURE_LABEL_LIST
                    ],
                    on_select=on_select,
                ),
            ],
        )
