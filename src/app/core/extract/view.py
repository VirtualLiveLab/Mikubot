from discord import ui
from ductile.ui import LinkButton

from src.components.delete_button import DeleteButton


class DispandView(ui.View):
    def __init__(self, *, message_url: str, button_label: str) -> None:
        super().__init__(timeout=None)
        self.add_item(
            LinkButton(button_label, url=message_url),
        )
        self.add_item(DeleteButton())
