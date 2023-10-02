from collections.abc import Generator
from typing import TYPE_CHECKING, Any, Literal, overload

import discord
from discord import ui

from components.ui.state import State
from components.ui.view import View

from .type import ViewObjectDictWithAttachment, ViewObjectDictWithFiles

if TYPE_CHECKING:
    from components.ui.view import ViewObject


class BaseController:
    def __init__(self, *, timeout: float | None = 180) -> None:
        self.__view: View
        self.__raw_view = ui.View(timeout=timeout)
        self.__message: discord.Message

    async def send(self, view: View) -> None:
        # maybe validation for self.__view is needed
        self.__view = view
        # implement this in subclasses
        raise NotImplementedError

    async def sync(self) -> None:
        """
        Sync the message with current view.
        """
        # maybe validation for self.__view is needed
        d = self._process_view_for_discord("attachment")
        self.__message = await self.__message.edit(**d)

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

    async def wait(self) -> bool:
        return await self.__raw_view.wait()

    def _get_all_state_in_view(self) -> Generator[tuple[str, State[Any]], None, None]:
        for k, v in self.__view.__dict__.items():
            if isinstance(v, State):
                yield k, v

    @overload
    def _process_view_for_discord(self, mode: Literal["attachment"]) -> ViewObjectDictWithAttachment:
        ...

    @overload
    def _process_view_for_discord(self, mode: Literal["files"]) -> ViewObjectDictWithFiles:
        ...

    def _process_view_for_discord(
        self,
        mode: Literal["attachment", "files"],
    ) -> ViewObjectDictWithAttachment | ViewObjectDictWithFiles:
        """
        _process_view_for_discord is a helper function to process the view for Discord.

        Parameters
        ----------
        mode : Literal[&quot;attachment&quot;, &quot;files&quot;]
            The mode to process the view for Discord.

            If the mode is `attachment`, ViewObject.files will be put into the `attachments` key.

            If the mode is `files`, ViewObject.files will be put into the `files` key.

        Returns
        -------
        ViewObjectDictWithAttachment | ViewObjectDictWithFiles
            The processed view dictionary.
            This can be passed to `discord.abc.Messageable.send` or `discord.abc.Messageable.edit` and etc
            as unpacked keyword arguments.
        """
        view_object: ViewObject = self.__view.render()

        if mode == "attachment":
            d_attachment: ViewObjectDictWithAttachment = {}
            d_attachment["content"] = view_object.content
            if view_object.embeds:
                d_attachment["embeds"] = view_object.embeds
            if view_object.files:
                d_attachment["attachments"] = view_object.files
            if view_object.components:
                v = self.__raw_view
                v.clear_items()
                for child in view_object.components:
                    v.add_item(child)
                d_attachment["view"] = v
            return d_attachment

        d_file: ViewObjectDictWithFiles = {}
        d_file["content"] = view_object.content
        if view_object.embeds:
            d_file["embeds"] = view_object.embeds
        if view_object.files:
            d_file["files"] = view_object.files

        if view_object.components:
            v = self.__raw_view
            v.clear_items()
            for child in view_object.components:
                v.add_item(child)
            d_file["view"] = v
        return d_file
