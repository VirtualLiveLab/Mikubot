import contextlib
import os
import re
from collections.abc import Iterable
from datetime import datetime
from typing import Any, TypedDict

import discord
from discord import Client, Message
from glom import glom
from notion_client import APIResponseError
from notion_client import AsyncClient as NotionAsyncClient
from notion_client.client import ClientOptions
from notion_client.helpers import is_full_database, is_full_page

from src.packages.url_extractor import IUrlAsyncProcessor
from src.utils.finder import Finder
from src.utils.logger import get_my_logger


class DiscordProcessor(IUrlAsyncProcessor[Message]):
    def __init__(self, client: Client) -> None:
        self._client = client
        self._finder = Finder(client)

    async def from_matches_async(self, matches: Iterable[re.Match[str]]) -> list[Message]:
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
        if not isinstance(
            channel,
            discord.TextChannel | discord.VoiceChannel | discord.StageChannel | discord.Thread,
        ):
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
    image: str | None


class NotionProcessor(IUrlAsyncProcessor[NotionPage]):
    def __init__(self) -> None:
        self.__client = NotionAsyncClient(options=ClientOptions(auth=os.getenv("NOTION_TOKEN")))
        self.__logger = get_my_logger(self.__class__.__name__)

    async def from_matches_async(self, matches: Iterable[re.Match[str]]) -> list[NotionPage]:
        page_ids = [pid for m in matches if isinstance((pid := m.group("page_uuid")), str)]
        self.__logger.debug("page_ids: %s", page_ids)

        full_pages: list[NotionPage] = []
        for pid in page_ids:
            try:
                resp_as_page = await self.__client.pages.retrieve(pid)
            except APIResponseError:
                self.__logger.warning("page not found for id: %s", pid)
            except Exception:
                self.__logger.exception("error while retrieving page: %s")
            else:
                if is_full_page(resp_as_page):
                    self.__logger.debug("full page retrieved.")
                    full_pages.append(self._process_page_object(resp_as_page))
                continue

            try:
                resp_as_db = await self.__client.databases.retrieve(pid)
            except APIResponseError:
                self.__logger.warning("database not found for id: %s", pid)
            except Exception:
                self.__logger.exception("error while retrieving database: %s")
            else:
                if is_full_database(resp_as_db):
                    self.__logger.debug("full database retrieved.")
                    full_pages.append(self._process_database_object(resp_as_db))
                continue

            self.__logger.warning("neither page nor database found for id: %s", pid)
            continue

        return full_pages

    def _process_page_object(self, obj: dict[str, Any]) -> NotionPage:
        url = self._get_safe_url(obj)
        title = self._get_safe_page_title(obj)
        emoji = self._get_safe_emoji(obj)
        last_updated = self._get_safe_last_updated(obj)
        image = self._get_safe_image(obj)
        return {
            "url": url,
            "title": title,
            "emoji": emoji,
            "last_updated": last_updated,
            "image": image,
        }

    def _process_database_object(self, obj: dict[str, Any]) -> NotionPage:
        url = self._get_safe_url(obj)
        title = self._get_safe_db_title(obj)
        emoji = self._get_safe_emoji(obj)
        last_updated = self._get_safe_last_updated(obj)
        return {
            "url": url,
            "title": title,
            "emoji": emoji,
            "last_updated": last_updated,
            "image": None,
        }

    def _get_safe_url(self, obj: dict[str, Any]) -> str:
        return url if isinstance((url := glom(obj, "url", default="")), str) else ""

    def _get_safe_emoji(self, obj: dict[str, Any]) -> str | None:
        return emoji if isinstance((emoji := glom(obj, "icon.emoji", default=None)), str) else None

    def _get_safe_page_title(self, obj: dict[str, Any]) -> str:
        props = pd if isinstance(pd := obj.get("properties"), dict) else None
        if props is None:
            return ""
        title_keys = [k for k, v in props.items() if isinstance(v, dict) and v.get("type") == "title"]
        if len(title_keys) == 0 or not isinstance((title_key := title_keys[0]), str):
            return ""

        titles = glom(
            obj,
            {"titles": (f"properties.{title_key}.title", ["plain_text"])},
            default={"titles": []},
        )
        if (
            isinstance(titles, dict)
            and isinstance((t_arr := titles.get("titles")), list)
            and len(t_arr) > 0
            and isinstance((t := t_arr[0]), str)
        ):
            return t
        return ""

    def _get_safe_db_title(self, obj: dict[str, Any]) -> str:
        titles = glom(
            obj,
            {"titles": ("title", ["plain_text"])},
            default={"titles": []},
        )
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

    def _get_safe_image(self, obj: dict[str, Any]) -> str | None:
        cover_type = t if isinstance((t := glom(obj, "cover.type", default=None)), str) else None
        if cover_type is None:
            return None

        match cover_type:
            case "external":
                return url if isinstance((url := glom(obj, "cover.external.url", default=None)), str) else None
            case "file":
                return url if isinstance((url := glom(obj, "cover.file.url", default=None)), str) else None
            case _:
                return None
