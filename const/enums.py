from enum import IntEnum


class Color(IntEnum):
    MIKU = 0x66DDCC
    WARNING = 0xFF0000
    SUCCESS = 0x00FF00


class Channel(IntEnum):
    GENERAL = 1089948444531097791
    ANNOUNCE = 1090159702870081638
    ROLE = 1095718001283706940


class Role(IntEnum):
    BUHI_MINOU = 1089948443444781121
    ADMIN = 1089948443465764936
    KAIKEI = 1089948443444781122