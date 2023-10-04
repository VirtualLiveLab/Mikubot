import asyncio
from typing import TYPE_CHECKING

import discord
from pydantic import BaseModel, ConfigDict, Field

from utils.logger import get_my_logger

# from components.ui.state import State

if TYPE_CHECKING:
    from components.ui.controller.controller import ViewController


class ViewObject(BaseModel):
    content: str = Field(default="")
    embeds: list[discord.Embed] | None = Field(default=None)
    files: list[discord.File] | None = Field(default=None)
    components: list[discord.ui.Item] | None = Field(default=None)

    model_config = ConfigDict(arbitrary_types_allowed=True)


class View:
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop | None = None,
    ) -> None:
        self._loop = loop or asyncio.get_event_loop()
        self._controller: ViewController | None = None
        self.__logger = get_my_logger(__name__)

    def render(self) -> ViewObject:
        return ViewObject()

    def sync(self) -> None:
        if self._controller:
            self._loop.create_task(self._controller.sync())
        else:
            self.__logger.warning("ViewSender is not set")

    def stop(self) -> None:
        if self._controller:
            self._controller.stop()
        else:
            self.__logger.warning("ViewSender is not set")

    async def on_error(self, interaction: discord.Interaction, error: Exception, item: discord.ui.Item) -> None:
        """
        on_error is called when an error occurs in the view.

        Parameters
        ----------
        interaction : `discord.Interaction`
            The interaction that caused the error.
        error : `Exception`
            The error that occurred.
        item : `discord.ui.Item`
            The item that caused the error.
        """

    async def on_timeout(self) -> None:
        """
        on_timeout is called when the view times out.
        """
