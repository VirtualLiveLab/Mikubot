from traceback import print_exc
from typing import TYPE_CHECKING

import discord
from ductile.ui import Modal, TextInput

if TYPE_CHECKING:
    from ductile.types import ModalCallback


class OpinionView(discord.ui.View):
    def __init__(self, on_submit: "ModalCallback") -> None:
        super().__init__(timeout=None)
        self.__on_submit = on_submit

    @discord.ui.button(label="意見箱を開く", style=discord.ButtonStyle.gray, custom_id="app.core.opinion.view.open_opinion")
    async def open_opinion(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        try:
            await interaction.response.send_modal(OpinionModal(self.__on_submit))
        except Exception:  # noqa: BLE001
            print_exc()
            if interaction.response.is_done():
                await interaction.followup.send(
                    "エラーが発生しました。\n何度も続く場合は管理者に連絡してください。",
                    ephemeral=True,
                )
                return
            await interaction.response.send_message(
                "エラーが発生しました。\n何度も続く場合は管理者に連絡してください。",
                ephemeral=True,
            )


class OpinionModal(Modal):
    def __init__(self, on_submit: "ModalCallback") -> None:
        super().__init__(
            title="サークル運営についての意見箱",
            timeout=None,
            inputs=[
                TextInput(
                    "意見",
                    style={
                        "placeholder": "例: 〇〇を改善して欲しい",
                        "field": "long",
                    },
                    config={"max_length": 2000, "required": True},
                )
            ],
            on_submit=on_submit,
        )
