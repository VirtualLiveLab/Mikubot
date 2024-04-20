import discord
from discord import Embed, Interaction
from ductile import State, View, ViewObject
from ductile.controller import InteractionController, MessageableController
from ductile.ui import Button

from src.const.emoji import CIRCLE_EMOJI, CROSS_EMOJI
from src.const.enums import Color


class ConfirmUI:
    def __init__(self, *, title: str, description: str, default_result: bool = False) -> None:
        self.title = title
        self.description = description

        self.default_result = default_result

    async def send_and_wait(
        self,
        target: discord.abc.Messageable | Interaction,
        *,
        ephemeral: bool = False,
        timeout: float | None = None,
    ) -> bool:
        controller: InteractionController | MessageableController
        view = ConfirmView(self.title, self.description)

        if isinstance(target, Interaction):
            controller = InteractionController(view, interaction=target, ephemeral=ephemeral, timeout=timeout)
        else:
            controller = MessageableController(view, messageable=target, timeout=timeout)

        await controller.send()
        res = await controller.wait()

        return res.states.get("result", self.default_result)


class ConfirmView(View):
    def __init__(self, title: str, description: str) -> None:
        super().__init__()
        self.result = State[bool | None](None, self)

        self.title = title
        self.description = description

    def render(self) -> ViewObject:
        e = Embed(
            title=self.title,
            description=self.description,
            color=Color.MIKU,
        )

        async def handle_click(interaction: Interaction, *, value: bool) -> None:
            await interaction.response.defer()
            self.result.set_state(new_value=value)
            self.stop()

        async def handle_approve(interaction: Interaction) -> None:
            await handle_click(interaction, value=True)

        async def handle_reject(interaction: Interaction) -> None:
            await handle_click(interaction, value=False)

        return ViewObject(
            embeds=[e],
            components=[
                Button(
                    style={
                        "color": "grey",
                        "emoji": CIRCLE_EMOJI,
                        "disabled": self.result() is not None,
                    },
                    on_click=handle_approve,
                ),
                Button(
                    style={
                        "color": "grey",
                        "emoji": CROSS_EMOJI,
                        "disabled": self.result() is not None,
                    },
                    on_click=handle_reject,
                ),
            ],
        )
