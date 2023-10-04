from collections.abc import Awaitable, Callable
from typing import TypeAlias

import discord
from discord.app_commands import AppCommandChannel, AppCommandThread

__all__ = [
    "InteractionCallback",
    "SelectCallback",
    "ChannelSelectCallback",
    "RoleSelectCallback",
    "MentionableSelectCallback",
    "UserSelectCallback",
    "ModalCallback",
]


InteractionCallback: TypeAlias = Callable[[discord.Interaction], Awaitable[None]]

# SelectCallback
SelectCallback: TypeAlias = Callable[[discord.Interaction, list[str]], Awaitable[None]]
ChannelSelectCallback: TypeAlias = Callable[
    [discord.Interaction, list[AppCommandChannel | AppCommandThread]],
    Awaitable[None],
]
RoleSelectCallback: TypeAlias = Callable[
    [discord.Interaction, list[discord.Role]],
    Awaitable[None],
]
MentionableSelectCallback: TypeAlias = Callable[
    [discord.Interaction, list[discord.Role | discord.Member | discord.User]],
    Awaitable[None],
]
UserSelectCallback: TypeAlias = Callable[[discord.Interaction, list[discord.User | discord.Member]], Awaitable[None]]

# ModalCallback
ModalCallback: TypeAlias = Callable[[discord.Interaction, dict[str, str]], Awaitable[None]]
