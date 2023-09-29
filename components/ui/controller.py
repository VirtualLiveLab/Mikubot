from collections.abc import Generator
from typing import Any, TypedDict

import discord
from discord import ui

from .state import State
from .view import View, ViewObject


class ViewObjectDict(TypedDict, total=False):
    """
    ViewObjectDict is a type hint for the dictionary that is used to send a view to Discord.

    This can be passed to `discord.abc.Messageable.send` as unpacked keyword arguments.

    Accessing the keys are not recommended since the existence of the keys are not guaranteed.

    Example
    -------
    ```py
    d: ViewObjectDict = {
        "content": "Hello, world!",
        "embeds": [discord.Embed(title="Hello, world!")],
    }
    await ctx.send(**d)
    """

    content: str
    embeds: list[discord.Embed]
    files: list[discord.File]
    view: ui.View


class ViewControllerBase:
    def __init__(self, view: View, timeout: float | None = 180) -> None:
        self.__view = view
        self.__raw_view = ui.View(timeout=timeout)

    async def send(self, target: discord.abc.Messageable) -> None:
        # await target.send(**self._process_view_for_discord())
        raise NotImplementedError

    def stop(self) -> dict[str, Any]:
        """
        Stop the view and return the state of all states in the view.

        Returns
        -------
        dict[str, Any]
            The state of all states in the view.
            Keys are the names of the states.
        """
        self.__raw_view.stop()

        d = {}
        for key, state in self._get_all_state_in_view():
            d[key] = state.get_state()
        return d

    async def wait(self) -> None:
        await self.__raw_view.wait()

    def _process_view_for_discord(self) -> ViewObjectDict:
        view_object: ViewObject = self.__view.render()
        d: ViewObjectDict = {}

        d["content"] = view_object.content
        if view_object.embeds:
            d["embeds"] = view_object.embeds
        if view_object.files:
            d["files"] = view_object.files

        if view_object.components:
            v = self.__raw_view
            v.clear_items()
            for child in view_object.components:
                v.add_item(child)
            d["view"] = v

        return d

    def _get_all_state_in_view(self) -> Generator[tuple[str, State[Any]], None, None]:
        for k, v in self.__view.__dict__.items():
            if isinstance(v, State):
                yield k, v
