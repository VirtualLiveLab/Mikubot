from enum import IntEnum, StrEnum


class Color(IntEnum):
    MIKU = 0x66DDCC
    WARNING = 0xFF0000
    SUCCESS = 0x00FF00


class TaskStatus(StrEnum):
    PENDING = "🔄"
    SUCCESS = "✅"
    ERROR = "❌"
