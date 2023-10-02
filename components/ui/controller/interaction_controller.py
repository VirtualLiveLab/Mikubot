import discord

from components.ui.view import View

from .controller import BaseController


class InteractionController(BaseController):
    def __init__(self, interaction: discord.Interaction, *, timeout: float | None = 180, ephemeral: bool = False) -> None:
        super().__init__(timeout=timeout)
        self.__interaction = interaction
        self.__ephemeral = ephemeral

    async def send(self, view: View) -> None:
        self.__view = view
        target = self.__interaction
        view_kwargs = self._process_view_for_discord("files")

        if target.is_expired():
            if target.channel is not None and not isinstance(target.channel, discord.CategoryChannel | discord.ForumChannel):
                self.__message = await target.channel.send(**view_kwargs)
            return

        if target.response.is_done():
            self.__message = await target.followup.send(**view_kwargs, ephemeral=self.__ephemeral, wait=True)
            return

        await target.response.send_message(**view_kwargs, ephemeral=self.__ephemeral)
        self.__message = await target.original_response()
        return
