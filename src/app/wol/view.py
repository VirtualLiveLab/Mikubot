from typing import TYPE_CHECKING

from discord import Embed, Interaction
from ductile import State, View
from ductile.ui import Button
from ductile.view import ViewObject

from .fn import ComputerBootResult, boot_computer, get_computer_status

if TYPE_CHECKING:
    from .fn import ComputerStatus


class WOLView(View):
    def __init__(self, initial_status: "ComputerStatus") -> None:
        super().__init__()
        self.status = State(initial_status, self)
        self.disabled = State(False, self)  # noqa: FBT003

    async def handle_wol_left(self, interaction: Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        res = await boot_computer("left")

        match res:
            case ComputerBootResult.STARTED:
                self.status.set_state(lambda c: {**c, "left": True})
                await interaction.followup.send("左PCの起動を開始しました。", ephemeral=True)
            case ComputerBootResult.CANCELED:
                await interaction.followup.send("左PCは既に起動しています。", ephemeral=True)
            case ComputerBootResult.ERROR:
                await interaction.followup.send("エラーが発生しました。", ephemeral=True)

    async def handle_wol_right(self, interaction: Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        res = await boot_computer("right")

        match res:
            case ComputerBootResult.STARTED:
                self.status.set_state(lambda c: {**c, "right": True})
                await interaction.followup.send("右PCの起動を開始しました。", ephemeral=True)
            case ComputerBootResult.CANCELED:
                await interaction.followup.send("右PCは既に起動しています。", ephemeral=True)
            case ComputerBootResult.ERROR:
                await interaction.followup.send("エラーが発生しました。", ephemeral=True)

    async def handle_refresh(self, interaction: Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        current_status = await get_computer_status()
        self.status.set_state(current_status)
        await interaction.followup.send("状態を更新しました。", ephemeral=True)

    async def handle_wol_exit(self, interaction: Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        self.disabled.set_state(True)
        self.stop()

    def render(self) -> ViewObject:
        def get_label(status: bool | None) -> str:
            match status:
                case True:
                    return "✅ 起動済み"
                case False:
                    return "❌ 停止中"
                case None:
                    return "❓ 不明"

        e = Embed(
            title="部室PC遠隔起動",
            description="部室のPCを遠隔で起動できます。\nただし、Botでは起動処理が実行されたかまでしか確認できないので、\n実際に起動したかどうかはAnyDeskなどで確認してください。",
        )
        e.add_field(name="左PC", value=get_label(self.status()["left"]))
        e.add_field(name="右PC", value=get_label(self.status()["right"]))

        return ViewObject(
            embeds=[e],
            components=[
                Button(
                    "左PCを起動する",
                    custom_id="wol_left",
                    style={"color": "blurple", "disabled": self.disabled() or bool(self.status()["left"]), "row": 0},
                    on_click=self.handle_wol_left,
                ),
                Button(
                    "右PCを起動する",
                    custom_id="wol_right",
                    style={"color": "blurple", "disabled": self.disabled() or bool(self.status()["right"]), "row": 0},
                    on_click=self.handle_wol_right,
                ),
                Button(
                    "表示を更新する",
                    custom_id="wol_refresh",
                    style={"color": "green", "disabled": self.disabled(), "row": 0, "emoji": "🔄"},
                    on_click=self.handle_refresh,
                ),
                Button(
                    "操作を終了する",
                    custom_id="wol_exit",
                    style={"color": "red", "disabled": self.disabled(), "row": 1},
                    on_click=self.handle_wol_exit,
                ),
            ],
        )
