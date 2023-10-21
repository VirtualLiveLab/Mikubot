from uuid import UUID

from discord import Embed, Interaction, ui
from ductile import State, View, ViewObject
from ductile.controller import InteractionController
from ductile.types import InteractionCallback
from ductile.ui import Button, LinkButton

from const.emoji import WASTE_BASKET
from const.enums import Color
from utils.logger import get_my_logger

from .type import UserVoteStatus
from .vote import OptionId, Vote, VoteOption


class VotePanel(View):
    def __init__(self, *, question: str, options: list[VoteOption]) -> None:
        super().__init__()
        self.__question = question
        self.__options = options
        self.__vote = Vote(options=options)
        self.__logger = get_my_logger(__name__)

    def render(self) -> ViewObject:
        async def get_user_vote(interaction: Interaction) -> None:
            await interaction.response.defer(ephemeral=True)
            user_vote_view = UserVoteView(
                options=self.__options,
                prev_chosen=self.__vote.get_user_vote(user_id=interaction.user.id),
                panel_url=interaction.message.jump_url if interaction.message else None,
            )
            controller = InteractionController(user_vote_view, interaction=interaction, timeout=120, ephemeral=True)
            await controller.send()
            _, states = await controller.wait()
            self.__logger.debug(repr(states))
            res = states["chosen"] if "chosen" in states and isinstance(states["chosen"], UUID | None) else None
            self.__logger.debug(repr(res))
            if res is not None:
                self.__vote.vote(user_id=interaction.user.id, option_id=res)
            else:
                self.__vote.devote(user_id=interaction.user.id)
            self.sync()

        e = Embed(
            title=self.__question,
            description="投票ボタンを押した後、選択肢を選んでください。",
            color=Color.MIKU,
        )
        for opt in self.__options:
            e.add_field(
                name=f"{opt.emoji} {opt.label}",
                value=f"票数: {self.__vote.get_number_of_vote(option_id=opt.option_id)}",
                inline=True,
            )

        return ViewObject(embeds=[e], components=[Button("投票", style={"color": "green"}, on_click=get_user_vote)])


class UserVoteView(View):
    def __init__(self, *, options: list[VoteOption], prev_chosen: OptionId | None, panel_url: str | None) -> None:
        super().__init__()
        self.__options = options
        self.__prev_chosen = prev_chosen
        self.__panel_url = panel_url
        self.status = UserVoteStatus.NOT_YET
        self.chosen = State[OptionId | None](None, self)

    def get_vote_handler(self, option: VoteOption) -> InteractionCallback:
        async def handler(interaction: Interaction) -> None:
            await interaction.response.defer()
            self.status = UserVoteStatus.VOTE_COMPLETE
            self.terminate(option.option_id)

        return handler

    async def devote_handler(self, interaction: Interaction) -> None:
        await interaction.response.defer()
        self.status = UserVoteStatus.VOTE_REMOVED
        self.terminate(None)

    async def on_timeout(self) -> None:
        self.status = UserVoteStatus.VOTE_TIMEOUT
        self.terminate(self.__prev_chosen)

    async def on_error(self, interaction: Interaction, _e: Exception, _i: ui.Item) -> None:
        await interaction.response.defer()
        self.status = UserVoteStatus.VOTE_ERROR
        self.terminate(self.__prev_chosen)

    def terminate(self, final_state: OptionId | None) -> None:
        self.chosen.set_state(final_state)
        self.stop()

    def render(self) -> ViewObject:
        match self.status:
            case UserVoteStatus.NOT_YET:
                return self._render_not_yet()
            case UserVoteStatus.VOTE_COMPLETE:
                return self._render_vote_complete()
            case UserVoteStatus.VOTE_REMOVED:
                return self._render_vote_removed()
            case UserVoteStatus.VOTE_TIMEOUT:
                return self._render_vote_timeout()
            case UserVoteStatus.VOTE_ERROR:
                return self._render_vote_error()

    def _render_not_yet(self) -> ViewObject:
        return ViewObject(
            embeds=[Embed(title="投票", description="投票したい選択肢のボタンを押してください。")],
            components=[
                *[
                    Button(
                        style={"color": "grey", "emoji": option.emoji, "disabled": self.__prev_chosen == option.option_id},
                        on_click=self.get_vote_handler(option),
                    )
                    for option in self.__options
                ],
                Button(
                    "投票取り消し",
                    style={"color": "red", "emoji": WASTE_BASKET, "disabled": self.__prev_chosen is None, "row": 4},
                    on_click=self.devote_handler,
                ),
            ],
        )

    def _render_vote_complete(self) -> ViewObject:
        return ViewObject(
            embeds=[
                Embed(
                    title="投票",
                    description="投票が完了しました。\n投票を変更する場合は、再度投票パネルのボタンを押してください。",
                    color=Color.SUCCESS,
                ),
            ],
            components=[self.vote_panel_button()],
        )

    def _render_vote_removed(self) -> ViewObject:
        return ViewObject(
            embeds=[
                Embed(
                    title="投票",
                    description="投票を取り消しました。\nもう一度投票する場合は、再度投票パネルのボタンを押してください。",
                    color=Color.SUCCESS,
                ),
            ],
            components=[self.vote_panel_button()],
        )

    def _render_vote_timeout(self) -> ViewObject:
        return ViewObject(
            embeds=[
                Embed(
                    title="投票",
                    description="操作がなかったためタイムアウトしました。\nもう一度投票する場合は、再度投票パネルのボタンを押してください。",
                    color=Color.MIKU,
                ),
            ],
            components=[self.vote_panel_button()],
        )

    def _render_vote_error(self) -> ViewObject:
        return ViewObject(
            embeds=[
                Embed(
                    title="投票",
                    description="エラーが発生しました。\nもう一度投票する場合は、再度投票パネルのボタンを押してください。",
                    color=Color.WARNING,
                ),
            ],
            components=[
                self.vote_panel_button(),
            ],
        )

    def vote_panel_button(self) -> LinkButton:
        return LinkButton("投票パネルへ戻る", url=self.__panel_url or "")
