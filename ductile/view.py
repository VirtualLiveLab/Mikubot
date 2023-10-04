import asyncio
from typing import TYPE_CHECKING

import discord
from pydantic import BaseModel, ConfigDict, Field

from .utils import get_logger

# from components.ui.state import State

if TYPE_CHECKING:
    from .controller import ViewController


__all__ = [
    "View",
    "ViewObject",
]


class ViewObject(BaseModel):
    """
    A class representing a view object that can be sent as a message in Discord.

    Attributes:
    -----------
    content : `str`
        The content of the message.
    embeds : `list[discord.Embed] | None`
        A list of embeds to be included in the message.
    files : `list[discord.File] | None`
        A list of files to be included in the message.
    components : `list[discord.ui.Item] | None`
        A list of UI components to be included in the message.
    """

    content: str = Field(default="")
    embeds: list[discord.Embed] | None = Field(default=None)
    files: list[discord.File] | None = Field(default=None)
    components: list[discord.ui.Item] | None = Field(default=None)

    model_config = ConfigDict(arbitrary_types_allowed=True)


class View:
    """
    The View class represents the user interface of the UI. It is responsible for rendering the UI and
    handling user interactions.

    Attributes
    -------
    message : `discord.Message | None`
        The message containing the UI. None if the UI has not been sent yet.

    Methods
    -------
    render() -> `ViewObject`:
        Renders the UI and returns a `ViewObject` representing the UI.
    sync() -> `None`:
        Synchronizes the view with the controller.
    stop() -> `None`:
        Stops the view.
    on_error(interaction: `discord.Interaction`, error: `Exception`, item: `discord.ui.Item`) -> `None`:
        Called when an error occurs in the view.
    on_timeout() -> `None`:
        Called when the view times out.
    """

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop | None = None,
    ) -> None:
        self._loop = loop or asyncio.get_event_loop()
        self._controller: ViewController | None = None
        self.__logger = get_logger(__name__)

    def render(self) -> ViewObject:
        """
        Renders the view and returns a ViewObject. This method is called by `Controller`.

        Returns
        -------
        ViewObject: The rendered view.
        """
        return ViewObject()

    def sync(self) -> None:
        """
        Synchronize the view with the controller. This method is called by `State` when its value changes.
        """
        if self._controller:
            self._loop.create_task(self._controller.sync())
        else:
            self.__logger.warning("Controller is not set")

    def stop(self) -> None:
        """
        Stops the view. This method is called by child components implicitly.
        """
        if self._controller:
            self._controller.stop()
        else:
            self.__logger.warning("Controller is not set")

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
