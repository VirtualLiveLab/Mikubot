from typing import TYPE_CHECKING

from discord import Embed, Interaction
from ductile import State, View, ViewObject
from ductile.ui import Button, RoleSelect

from src.const.enums import Color

if TYPE_CHECKING:
    from discord import Role


class AddRolesToThreadView(View):
    def __init__(self, target_mention: str) -> None:
        super().__init__()
        self.target_mention = target_mention
        self.accepted = State[bool](False, self)  # noqa: FBT003
        self.disabled = State[bool](False, self)  # noqa: FBT003
        self.selected = State["list[Role]"]([], self)

    async def on_timeout(self) -> None:
        self.accepted.set_state(False)  # noqa: FBT003
        return await super().on_timeout()

    def render(self) -> ViewObject:
        async def handle_select(interaction: "Interaction", values: "list[Role]") -> None:
            await interaction.response.defer()
            self.selected.set_state(values)

        async def handle_cancel(interaction: Interaction) -> None:
            await interaction.response.defer()
            stop_view()

        async def handle_start(interaction: Interaction) -> None:
            await interaction.response.defer()
            self.accepted.set_state(True)  # noqa: FBT003
            stop_view()

        def stop_view() -> None:
            self.disabled.set_state(True)  # noqa: FBT003
            self.stop()

        def embed() -> Embed:
            e = Embed(
                title="スレッドにロールを追加",
                description="追加したいロールを選択してください。(最大5個まで)",
                color=Color.MIKU,
            )
            e.add_field(name="対象スレッド", value=self.target_mention)
            e.add_field(name="選択されているロール", value="\n".join([r.mention for r in self.selected()]))
            return e

        return ViewObject(
            embeds=[embed()],
            components=[
                RoleSelect(
                    config={"min_values": 1, "max_values": 5},
                    style={"placeholder": "追加したいロールを選択してください。", "row": 0, "disabled": self.disabled()},
                    on_select=handle_select,
                ),
                Button("キャンセル", style={"color": "red", "row": 2, "disabled": self.disabled()}, on_click=handle_cancel),
                Button(
                    "実行",
                    style={"disabled": self.disabled() or self.selected() == [], "color": "green", "row": 2},
                    on_click=handle_start,
                ),
            ],
        )
