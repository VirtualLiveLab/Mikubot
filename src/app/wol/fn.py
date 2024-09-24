import os
from enum import Enum
from typing import Literal, TypeAlias, TypedDict

import aiohttp

# https://www.notion.so/virtual-live-lab/19805a3d88d94ba5b47408c054a2e9
LEFT_PC_MAC_ADDRESS = "04:7C:16:01:41:A7"
RIGHT_PC_MAC_ADDRESS = "FC:34:97:BA:12:F1"

LEFT_PC_IP_ADDRESS = "192.168.39.31"
RIGHT_PC_IP_ADDRESS = "192.168.39.30"

ComputerType: TypeAlias = Literal["left", "right"]


class ComputerStatus(TypedDict):
    left: bool | None
    right: bool | None


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
            "https://wol.vlldev.com/check_status", params={"ip_address": LEFT_PC_IP_ADDRESS, "test_type": "icmp"}
        ) as left_response,
        session.get(
            "https://wol.vlldev.com/check_status", params={"ip_address": RIGHT_PC_IP_ADDRESS, "test_type": "icmp"}
        ) as right_response,
    ):
        left_is_wake = convert_status_str_to_bool(await left_response.text())
        right_is_wake = convert_status_str_to_bool(await right_response.text())
        return {"left": left_is_wake, "right": right_is_wake}


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
            data={"mac_address": LEFT_PC_MAC_ADDRESS if computer == "left" else RIGHT_PC_MAC_ADDRESS},
        ) as response,
    ):
        return ComputerBootResult(await response.text())


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
