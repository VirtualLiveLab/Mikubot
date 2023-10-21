from enum import Enum, auto


class UserVoteStatus(Enum):
    NOT_YET = auto()
    VOTE_COMPLETE = auto()
    VOTE_REMOVED = auto()
    VOTE_TIMEOUT = auto()
    VOTE_ERROR = auto()
