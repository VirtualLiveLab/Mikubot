from discord import ui

from src.components.delete_button import DeleteButton


class DeleteView(ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.add_item(DeleteButton())
