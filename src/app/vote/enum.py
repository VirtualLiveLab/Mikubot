from enum import Enum, auto  # noqa: A005


class UserVoteStatus(Enum):
    NOT_YET = auto()
    VOTE_COMPLETE = auto()
    VOTE_REMOVED = auto()
    VOTE_TIMEOUT = auto()
    VOTE_ERROR = auto()
