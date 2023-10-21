from uuid import UUID

from discord import Embed, Interaction, ui
from ductile import State, View, ViewObject
from ductile.controller import InteractionController
from ductile.types import InteractionCallback
from ductile.ui import Button, LinkButton

from src.components.confirm_ui import ConfirmUI
from src.const.emoji import CIRCLE_EMOJI, WASTE_BASKET
from src.const.enums import Color

from .enum import UserVoteStatus
from .manager import OptionId, VoteManager, VoteOption


class VotePanel(View):
    def __init__(self, *, question: str, options: list[VoteOption], is_anonymous: bool) -> None:
        super().__init__()
        self.__question = question
        self.__options = options
        self.__manager = VoteManager(options=options, is_anonymous=is_anonymous)

    def render(self) -> ViewObject:
        async def get_user_vote(interaction: Interaction) -> None:
            await interaction.response.defer(ephemeral=True)
            user_vote_view = UserVoteView(
                options=self.__options,
                prev_chosen=self.__manager.get_user_vote(user_id=interaction.user.id),
                panel_url=interaction.message.jump_url if interaction.message else None,
            )
            controller = InteractionController(user_vote_view, interaction=interaction, timeout=120, ephemeral=True)
            await controller.send()
            _, states = await controller.wait()
            res = states["chosen"] if "chosen" in states and isinstance(states["chosen"], UUID | None) else None

            if res is not None:
                self.__manager.vote(user_id=interaction.user.id, option_id=res)
            else:
                self.__manager.devote(user_id=interaction.user.id)
            self.sync()

        async def close(interaction: Interaction) -> None:
            await interaction.response.defer(ephemeral=True)
            conf_ui = ConfirmUI(
                title="投票を締め切りますか？",
                description=f"{CIRCLE_EMOJI}を押すと投票が締め切られます。",
                default_result=False,
            )
            res = await conf_ui.send_and_wait(interaction, ephemeral=True, timeout=120)
            if not res:
                return

            if self.__manager.is_open:
                self.__manager.is_open = False
            self.sync()
            self.stop()

        def embed_is_open() -> Embed:
            all_counts = self.__manager.get_count_of_all_options()
            e = Embed(
                title=self.__question,
                description="投票ボタンを押した後、選択肢を選んでください。",
                color=Color.MIKU,
            )
            for opt in self.__options:
                e.add_field(
                    name=f"{opt.emoji} {opt.label}",
                    value=f"票数: {all_counts[opt.option_id]}",
                    inline=True,
                )
            return e

        def embed_is_closed() -> Embed:
            all_counts = self.__manager.get_count_of_all_options()
            e = Embed(
                title=self.__question,
                description="この投票は締め切られました。",
                color=Color.MIKU,
            )
            for opt in sorted(self.__options, key=lambda o: all_counts[o.option_id], reverse=True):
                e.add_field(
                    name=f"{opt.emoji} {opt.label}",
                    value=f"票数: {all_counts[opt.option_id]}",
                    inline=True,
                )
            return e

        return ViewObject(
            embeds=[embed_is_open() if self.__manager.is_open else embed_is_closed()],
            components=[
                Button("投票", style={"color": "green", "disabled": not self.__manager.is_open}, on_click=get_user_vote),
                Button("締め切り", style={"color": "red", "disabled": not self.__manager.is_open}, on_click=close),
            ],
        )


class UserVoteView(View):
    def __init__(self, *, options: list[VoteOption], prev_chosen: OptionId | None, panel_url: str | None) -> None:
        super().__init__()
        self.__options = options
        self.__prev_chosen = prev_chosen
        self.__panel_url = panel_url
        self.__status = UserVoteStatus.NOT_YET
        self.chosen = State[OptionId | None](None, self)

    def get_vote_handler(self, option: VoteOption) -> InteractionCallback:
        async def handler(interaction: Interaction) -> None:
            await interaction.response.defer()
            self.__status = UserVoteStatus.VOTE_COMPLETE
            self.terminate(result=option.option_id)

        return handler

    async def devote_handler(self, interaction: Interaction) -> None:
        await interaction.response.defer()
        self.__status = UserVoteStatus.VOTE_REMOVED
        self.terminate(result=None)

    async def on_timeout(self) -> None:
        self.__status = UserVoteStatus.VOTE_TIMEOUT
        self.terminate(result=self.__prev_chosen)

    async def on_error(self, interaction: Interaction, _e: Exception, _i: ui.Item) -> None:
        await interaction.response.defer()
        self.__status = UserVoteStatus.VOTE_ERROR
        self.terminate(result=self.__prev_chosen)

    def terminate(self, *, result: OptionId | None) -> None:
        self.chosen.set_state(result)
        self.stop()

    def render(self) -> ViewObject:
        match self.__status:
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
            embeds=[
                Embed(
                    title="投票",
                    description="投票したい選択肢のボタンを押してください。",
                    color=Color.MIKU,
                ),
            ],
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
