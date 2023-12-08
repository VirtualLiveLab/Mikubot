from typing import Annotated, TypeAlias
from uuid import uuid4

from pydantic import UUID4, BaseModel, Field

OptionId: TypeAlias = Annotated[UUID4, "OptionId"]
VotedUserId: TypeAlias = Annotated[int, "VotedUserId"]


class VoteOption(BaseModel):
    emoji: str = Field(frozen=True)
    label: str = Field(frozen=True)

    # this field will be generated automatically.
    option_id: UUID4 = Field(default_factory=uuid4, frozen=True)


class VoteManager:
    def __init__(self, *, options: list[VoteOption], is_anonymous: bool) -> None:
        super().__init__()
        self.__users_of_options: dict[OptionId, list[VotedUserId]] = {o.option_id: [] for o in options}
        self.__user_votes: dict[VotedUserId, OptionId | None] = {}
        self.is_open: bool = True
        self.is_anonymous: bool = is_anonymous

    def get_count_of_option(self, *, option_id: OptionId) -> int:
        users = self.__users_of_options.get(option_id, [])
        return len(users)

    def get_count_of_all_options(self) -> dict[OptionId, int]:
        users = self.__users_of_options.copy()
        return {k: len(v) for k, v in users.items()}

    def get_users_of_option(self, *, option_id: OptionId) -> list[VotedUserId]:
        """
        選択肢に投票したユーザーのリストを返す。
        匿名投票でアクセスした場合は例外を発生させる。

        Parameters
        ----------
        option_id : OptionId
            対象の選択肢ID

        Returns
        ----------
        list[VotedUserId]
            投票したユーザーのリスト
        """
        self._deny_if_anonymous()
        return self.__users_of_options.get(option_id, [])

    def get_users_of_all_options(self) -> dict[OptionId, list[VotedUserId]]:
        """
        選択肢ごとに投票したユーザーのリストを返す。
        匿名投票でアクセスした場合は例外を発生させる。

        Returns
        ----------
        dict[OptionId, list[VotedUserId]]
            選択肢ごとの投票したユーザーのリスト
        """
        self._deny_if_anonymous()
        return self.__users_of_options.copy()

    def get_user_vote(self, *, user_id: VotedUserId) -> OptionId | None:
        """
        ユーザーの投票情報を返す。このメソッドは`UserVoteView`で必要なので、
        匿名投票であっても例外を発生させない。

        Parameters
        ----------
        user_id : VotedUserId
            対象のユーザーID

        Returns
        -------
        OptionId | None
            ユーザーの投票情報。投票していない場合は`None`を返す。
        """
        return self.__user_votes.get(user_id, None)

    def get_all_user_votes(self) -> dict[VotedUserId, OptionId | None]:
        """
        全ユーザーの投票情報を返す。このメソッドは`UserVoteView`で必要なので、
        匿名投票であっても例外を発生させない。

        Returns
        -------
        dict[VotedUserId, OptionId | None]
            全ユーザーの投票情報。ユーザーが投票していない場合はValueが`None`になる。
        """
        return self.__user_votes.copy()

    def vote(self, *, user_id: VotedUserId, option_id: OptionId) -> None:
        if not self.is_open:
            return

        self.devote(user_id=user_id)
        self.__users_of_options[option_id].append(user_id)
        self.__user_votes[user_id] = option_id

    def devote(self, *, user_id: VotedUserId) -> None:
        if not self.is_open:
            return

        option_id = self.__user_votes.get(user_id, None)
        if option_id is not None:
            self.__users_of_options[option_id].remove(user_id)
        self.__user_votes[user_id] = None

    def _deny_if_anonymous(self) -> None:
        """
        ユーザーの投票情報を返すメソッドを呼び出す際に、匿名投票の場合は例外を発生させる。

        Raises
        ------
        ValueError
            匿名投票の場合に発生する例外。
        """
        if self.is_anonymous:
            msg = "This operation is not allowed in anonymous vote."
            raise ValueError(msg)
