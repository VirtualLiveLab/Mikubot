import contextlib
import os
import re
from datetime import datetime
from typing import Any, TypedDict

import discord
from discord import Client, Message
from glom import glom
from notion_client import AsyncClient as NotionAsyncClient
from notion_client.client import ClientOptions
from notion_client.helpers import is_full_page

from src.utils.logger import get_my_logger

from .finder import Finder


class DiscordExtractor:
    def __init__(self, client: Client) -> None:
        self._client = client
        self._finder = Finder(client)

    async def from_matches(self, matches: set[re.Match[str]]) -> list[Message]:
        messages: list[Message] = []
        for ids in matches:
            if int(ids["guild"]) not in [g.id for g in self._client.guilds]:
                continue

            fetched_message = await self._fetch_message_from_id(
                channel_id=int(ids["channel"]),
                message_id=int(ids["message"]),
            )
            if fetched_message is not None:
                messages.append(fetched_message)
        return messages

    async def _fetch_message_from_id(self, *, channel_id: int, message_id: int) -> Message | None:
        channel = await self._finder.find_channel(channel_id)
        if not isinstance(channel, discord.TextChannel | discord.VoiceChannel | discord.StageChannel | discord.Thread):
            return None

        try:
            return await channel.fetch_message(message_id)
        except Exception:  # noqa: BLE001
            return None


class NotionPage(TypedDict):
    url: str
    title: str
    emoji: str | None
    last_updated: datetime | None


class NotionExtractor:
    def __init__(self) -> None:
        self.__client = NotionAsyncClient(options=ClientOptions(auth=os.getenv("NOTION_TOKEN")))
        self.__logger = get_my_logger(self.__class__.__name__)

    async def from_matches(self, matches: set[re.Match[str]]) -> list[NotionPage]:
        page_ids = [pid for m in matches if isinstance((pid := m.group("page_uuid")), str)]
        self.__logger.debug("page_ids: %s", page_ids)

        full_pages: list[NotionPage] = []
        for pid in page_ids:
            resp = await self.__client.pages.retrieve(pid)
            self.__logger.debug("page retrieved.")
            if is_full_page(resp):
                self.__logger.debug("is full page")
                full_pages.append(self._process_page_object(resp))

        return full_pages

    def _process_page_object(self, obj: dict[str, Any]) -> NotionPage:
        url: str = glom(obj, "url", default="")
        title = self._get_safe_title(obj)
        emoji: str | None = glom(obj, "icon.emoji", default=None)
        last_updated = self._get_safe_last_updated(obj)
        return {"url": url, "title": title, "emoji": emoji, "last_updated": last_updated}

    def _get_safe_title(self, obj: dict[str, Any]) -> str:
        titles = glom(obj, {"titles": ("properties.title.title", ["plain_text"])}, default={"titles": []})
        if (
            isinstance(titles, dict)
            and isinstance((t_arr := titles.get("titles")), list)
            and len(t_arr) > 0
            and isinstance((t := t_arr[0]), str)
        ):
            return t
        return ""

    def _get_safe_last_updated(self, obj: dict[str, Any]) -> datetime | None:
        dt: datetime | None = None

        last_edited = glom(obj, "last_edited_time", default=None)
        if isinstance(last_edited, str):
            with contextlib.suppress(ValueError):
                dt = datetime.fromisoformat(last_edited)

        if dt:
            return dt

        created = glom(obj, "created_time", default=None)
        if isinstance(created, str):
            with contextlib.suppress(ValueError):
                dt = datetime.fromisoformat(created)

        return dt
