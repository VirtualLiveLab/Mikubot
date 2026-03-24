import os
from enum import Enum
from typing import Literal, TypedDict

import aiohttp

# https://www.notion.so/virtual-live-lab/ddf6d9708a2e45469f675c37e6d09e28
type ComputerType = Literal["left", "right", "stream"]


class ComputerStatus(TypedDict):
    left: bool | None
    right: bool | None
    stream: bool | None


class ComputerAddresses(TypedDict):
    left: str
    right: str
    stream: str


PC_MAC_ADDRESSES: ComputerAddresses = {
    "left": "04:7C:16:01:41:A7",
    "right": "FC:34:97:BA:12:F1",
    "stream": "34:5A:60:A9:5F:CA",
}

PC_IP_ADDRESSES: ComputerAddresses = {
    "left": "192.168.39.31",
    "right": "192.168.39.30",
    "stream": "192.168.39.32",
}


def convert_status_str_to_bool(response_text: str) -> bool | None:
    match response_text:
        case "awake":
            return True
        case "asleep":
            return False
        case _:
            return None


async def get_computer_status() -> ComputerStatus:
    async with (
        get_cf_session() as session,
        session.get(
            "https://wol.vlldev.com/check_status", params={"ip_address": PC_IP_ADDRESSES["left"], "test_type": "icmp"}
        ) as left_response,
        session.get(
            "https://wol.vlldev.com/check_status", params={"ip_address": PC_IP_ADDRESSES["right"], "test_type": "icmp"}
        ) as right_response,
        session.get(
            "https://wol.vlldev.com/check_status", params={"ip_address": PC_IP_ADDRESSES["stream"], "test_type": "icmp"}
        ) as stream_response,
    ):
        left_is_wake = convert_status_str_to_bool(await left_response.text())
        right_is_wake = convert_status_str_to_bool(await right_response.text())
        stream_is_wake = convert_status_str_to_bool(await stream_response.text())
        return {"left": left_is_wake, "right": right_is_wake, "stream": stream_is_wake}


class ComputerBootResult(Enum):
    STARTED = "Magic Packet Sent !"
    CANCELED = "Computer is Already Awake"
    ERROR = "Unknown Error"

    # APIから帰ってきたレスポンスのtextから直接Enumを生成するので、予期せぬ値はすべてERRORにする
    @classmethod
    def _missing_(cls, value: object) -> "ComputerBootResult":  # noqa: ARG003
        return cls.ERROR


async def boot_computer(computer: ComputerType) -> ComputerBootResult:
    async with (
        get_cf_session() as session,
        session.post(
            "https://wol.vlldev.com/wakeup",
            data={"mac_address": PC_MAC_ADDRESSES[computer]},
        ) as response,
    ):
        res = await response.text()
        if ComputerBootResult.STARTED.value in res:
            return ComputerBootResult.STARTED
        if ComputerBootResult.CANCELED.value in res:
            return ComputerBootResult.CANCELED
        return ComputerBootResult.ERROR


class MissingEnvironmentValueError(Exception):
    def __init__(self) -> None:
        super().__init__("Required environment variables are not set.")


def get_cf_session() -> aiohttp.ClientSession:
    cf_id = os.getenv("CF_ACCESS_CLIENT_ID")
    cf_secret = os.getenv("CF_ACCESS_CLIENT_SECRET")

    if cf_id is None or cf_secret is None:
        raise MissingEnvironmentValueError

    headers = {"CF-Access-Client-Id": cf_id, "CF-Access-Client-Secret": cf_secret}
    return aiohttp.ClientSession(headers=headers)
