from discord import ui

from components.delete_button import DeleteButton
from ductile.ui import LinkButton


class DispandView(ui.View):
    def __init__(self, *, message_url: str) -> None:
        super().__init__(timeout=None)
        self.add_item(
            LinkButton("元のメッセージ", url=message_url),
        )
        self.add_item(DeleteButton())
