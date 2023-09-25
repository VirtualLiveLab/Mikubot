from discord import ButtonStyle, ui
from discord.interactions import Interaction

from const.emoji import WASTE_BASKET

DELETE_BUTTON_ID = "delete_button"


class DeleteButton(ui.Button):
    def __init__(
        self,
    ) -> None:
        super().__init__(style=ButtonStyle.red, custom_id=DELETE_BUTTON_ID, emoji=WASTE_BASKET, row=0)

    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.defer()
        await interaction.delete_original_response()
