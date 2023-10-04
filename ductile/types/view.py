from collections.abc import Awaitable, Callable
from typing import TypeAlias

import discord

__all__ = [
    "ViewErrorHandler",
    "ViewTimeoutHandler",
]

ViewErrorHandler: TypeAlias = Callable[[discord.Interaction, Exception, discord.ui.Item], Awaitable[None]]
ViewTimeoutHandler: TypeAlias = Callable[[], Awaitable[None]]
