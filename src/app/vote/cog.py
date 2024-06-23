from typing import TYPE_CHECKING, ClassVar

import discord
from discord import app_commands
from discord.ext import commands
from ductile.controller import InteractionController

from src.app.utils.callback import command_unavailable_callback
from src.utils.io import read_json

from .manager import VoteOption
from .view import VotePanel

if TYPE_CHECKING:
    # import some original class
    from src.app.bot import Bot


class Vote(commands.Cog):
    __RENAMED_OPTIONS: ClassVar[dict[str, str]] = {f"option{i}": f"選択肢{i}" for i in range(1, 11)}
    vote_app = app_commands.Group(name="vote", description="投票関連のコマンド")

    def __init__(self, bot: "Bot") -> None:
        self.bot = bot

    @vote_app.command(name="public", description="リアクション式投票(提供終了)")
    async def vote_public(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        await command_unavailable_callback(
            interaction,
            status="DEPRECATED",
            deprecated_alternative="Discord公式の投票機能(アプリを最新版にすれば利用できます)",
        )

    @vote_app.command(  # type: ignore[arg-type]
        name="anonymous",
        description="最大10択で匿名の投票を作成するよ！選択肢をすべて省略するとはい/いいえの投票になるよ！",
    )
    @app_commands.rename(**(__RENAMED_OPTIONS | {"question": "質問文"}))
    async def vote_anonymous(  # noqa: PLR0913
        self,
        interaction: discord.Interaction,
        question: str,
        option1: str | None = None,
        option2: str | None = None,
        option3: str | None = None,
        option4: str | None = None,
        option5: str | None = None,
        option6: str | None = None,
        option7: str | None = None,
        option8: str | None = None,
        option9: str | None = None,
        option10: str | None = None,
        # option11: str | None = None,
        # option12: str | None = None,
        # option13: str | None = None,
        # option14: str | None = None,
        # option15: str | None = None,
        # option16: str | None = None,
        # option17: str | None = None,
        # option18: str | None = None,
        # option19: str | None = None,
        # option20: str | None = None,
    ) -> None:
        await interaction.response.defer(ephemeral=False)
        if interaction.channel is None:
            return

        raw_options = [
            opt
            for opt in [
                option1,
                option2,
                option3,
                option4,
                option5,
                option6,
                option7,
                option8,
                option9,
                option10,
                # option11,
                # option12,
                # option13,
                # option14,
                # option15,
                # option16,
                # option17,
                # option18,
                # option19,
                # option20,
            ]
            if opt is not None and opt != ""
        ]

        emoji_dict = read_json(r"src/const/vote_emoji.json")
        if raw_options == []:
            option = [
                VoteOption(emoji=emoji_dict["0"], label="はい"),
                VoteOption(emoji=emoji_dict["1"], label="いいえ"),
            ]
        else:
            option = [VoteOption(emoji=emoji_dict[str(i)], label=raw_options[i]) for i in range(len(raw_options))]

        vote_panel = VotePanel(question=question, options=option, is_anonymous=True)
        controller = InteractionController(view=vote_panel, interaction=interaction, timeout=None, sync_interval=1)
        await controller.send()


async def setup(bot: "Bot") -> None:
    await bot.add_cog(Vote(bot))
