from typing import Annotated, TypeAlias
from uuid import uuid4

from pydantic import UUID4, BaseModel, Field

OptionId: TypeAlias = Annotated[UUID4, "OptionId"]
VotedUserId: TypeAlias = Annotated[int, "VotedUserId"]


class VoteOption(BaseModel):
    emoji: str
    label: str

    option_id: UUID4 = Field(default_factory=uuid4)


class Vote:
    def __init__(self, options: list[VoteOption]) -> None:
        super().__init__()
        self._options = options
        self._number_of_votes: dict[OptionId, int] = {o.option_id: 0 for o in options}
        self._user_votes: dict[VotedUserId, OptionId | None] = {}

    def get_number_of_vote(self, *, option_id: OptionId) -> int:
        return self._number_of_votes.get(option_id, -1)

    def get_all_number_of_vote(self) -> dict[OptionId, int]:
        return self._number_of_votes.copy()

    def get_user_vote(self, *, user_id: VotedUserId) -> OptionId | None:
        return self._user_votes.get(user_id, None)

    def get_all_user_votes(self) -> dict[VotedUserId, OptionId | None]:
        return self._user_votes.copy()

    def vote(self, *, user_id: VotedUserId, option_id: OptionId) -> None:
        self.devote(user_id=user_id)
        self._number_of_votes[option_id] += 1
        self._user_votes[user_id] = option_id

    def devote(self, *, user_id: VotedUserId) -> None:
        option_id = self._user_votes.get(user_id, None)
        if option_id is not None:
            self._number_of_votes[option_id] -= 1
        self._user_votes[user_id] = None
