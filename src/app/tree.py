from typing import TYPE_CHECKING

from discord import app_commands

if TYPE_CHECKING:
    from discord import Client, Interaction
    from discord.app_commands import AppCommandError


class BotCommandTree(app_commands.CommandTree):
    def __init__(self, client: "Client", *, fallback_to_global: bool = True) -> None:
        super().__init__(client, fallback_to_global=fallback_to_global)

    async def on_error(self, interaction: "Interaction[Client]", error: "AppCommandError") -> None:
        """
        TODO: Add logging here
        """
        return await super().on_error(interaction, error)
