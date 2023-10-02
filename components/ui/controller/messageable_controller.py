import discord

from components.ui.view import View

from .controller import BaseController


class MessageableController(BaseController):
    def __init__(self, messageable: discord.abc.Messageable, *, timeout: float | None = 180) -> None:
        super().__init__(timeout=timeout)
        self.__messageable = messageable

    async def send(self, view: View) -> None:
        self.__view = view
        target = self.__messageable
        view_kwargs = self._process_view_for_discord("files")

        self.__message = await target.send(**view_kwargs)
