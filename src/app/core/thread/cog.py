import asyncio
from typing import TYPE_CHECKING

from discord import AllowedMentions, Thread, app_commands
from discord.ext import commands
from ductile.controller import InteractionController

from src.app.utils.view import DeleteView
from src.utils.chunk import chunk_str_iter_with_max_length
from src.utils.finder import Finder

from .view import AddRolesToThreadView

if TYPE_CHECKING:
    # import some original class
    from discord import Interaction, Role

    from src.app.bot import Bot


class ThreadCog(commands.Cog):
    thread = app_commands.Group(name="thread", description="スレッド関連のコマンド")

    def __init__(self, bot: "Bot") -> None:
        self.bot = bot

    @app_commands.rename(target="スレッド")
    @app_commands.describe(target="追加先スレッド。補完に出なくてもIDを直打ちすれば入力できます。")
    @thread.command(name="add-role", description="スレッドに指定したロールのメンバーを追加します。")
    async def add_role_command(self, interaction: "Interaction", target: Thread) -> None:
        await interaction.response.defer()
        controller = InteractionController(
            AddRolesToThreadView(target_mention=target.mention),
            interaction=interaction,
            timeout=None,
        )
        await controller.send()
        _, state = await controller.wait()
        accepted: bool = state["accepted"]
        if not accepted:
            return
        selected_roles: list[Role] = state["selected"]
        # chunk_str_iter_with_max_lengthに渡す前に重複排除したいので、多少重くてもsetを使う
        member_mention_set: set[str] = {m.mention for r in selected_roles for m in r.members}

        thread = await Finder(self.bot).find_channel(target.id, expected_type=Thread)
        bot_msg = await thread.send(
            f"{thread.mention}に以下のロールを持つメンバーを追加します。\n\n{','.join([r.mention for r in selected_roles])}",
            silent=True,
            allowed_mentions=AllowedMentions.none(),
        )
        await asyncio.sleep(2)

        for string in chunk_str_iter_with_max_length(
            member_mention_set,
            max_length=2000,
            separator="\n",
        ):
            await bot_msg.edit(content=string)
            await asyncio.sleep(2)

        await bot_msg.edit(
            content=f"{thread.mention}に{len(member_mention_set)}人のメンバーを追加しました。\nこのメッセージは30秒後に自動で削除されます。",
            delete_after=30,
            view=DeleteView(),
        )

        return


async def setup(bot: "Bot") -> None:
    await bot.add_cog(ThreadCog(bot))
