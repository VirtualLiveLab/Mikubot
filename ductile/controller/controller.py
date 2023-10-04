from collections.abc import Generator
from typing import TYPE_CHECKING, Any, Literal, NamedTuple, overload

import discord

from ductile import State, View
from ductile.internal import _InternalView

from .type import ViewObjectDictWithAttachment, ViewObjectDictWithFiles

if TYPE_CHECKING:
    from ductile import ViewObject


class ViewResult(NamedTuple):
    timed_out: bool
    states: dict[str, Any]


class ViewController:
    def __init__(self, view: View, *, timeout: float | None = 180) -> None:
        self.__view = view
        view._controller = self  # noqa: SLF001
        self.__raw_view = _InternalView(timeout=timeout, on_error=self.__view.on_error, on_timeout=self.__view.on_timeout)
        self.__message: discord.Message | None = None

    @property
    def message(self) -> discord.Message | None:
        """
        return attached message with the View.

        Returns
        -------
        `discord.Message | None`
            The attached message. None if the View is not sent yet.
        """
        return self.__message

    @message.setter
    def message(self, value: discord.Message | None) -> None:
        self.__message = value

    async def send(self) -> None:
        # implement this in subclasses
        raise NotImplementedError

    async def sync(self) -> None:
        """
        Sync the message with current view.
        """
        if self.message is None:
            return

        # maybe validation for self.__view is needed
        d = self._process_view_for_discord("attachment")
        self.message = await self.message.edit(**d)

    def stop(self) -> None:
        """
        Stop the view and return the state of all states in the view.
        """
        self.__raw_view.stop()

    async def wait(self) -> ViewResult:
        """
        Wait for the view to stop and return the state of all states in the view.

        Returns
        -------
        `ViewResult(NamedTuple)`
            The result of the view.

            `timed_out` is True if the view timed out and False otherwise. same as `discord.ui.View.wait`.

            `states` is a dictionary of all states in the view.
        """
        timed_out = await self.__raw_view.wait()

        d = {}
        for key, state in self._get_all_state_in_view():
            d[key] = state.get_state()
        return ViewResult(timed_out, d)

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
