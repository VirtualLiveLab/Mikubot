import asyncio
from typing import TYPE_CHECKING

import discord
from discord import Embed, Member, app_commands
from discord.ext import commands
from ductile.controller import InteractionController

from src.const.enums import Color
from src.utils.chunk import chunk_str_iter_with_max_length

from .view import AndMentionView, RoleCheckView

if TYPE_CHECKING:
    # import some original class
    from src.app.bot import Bot


class Role(commands.Cog):
    role = app_commands.Group(name="role", description="ロール関連のコマンド")

    def __init__(self, bot: "Bot") -> None:
        self.bot = bot

    @role.command(name="check", description="ロールを確認します。")
    async def check_role(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        controller = InteractionController(
            RoleCheckView(),
            interaction=interaction,
            timeout=None,
            ephemeral=True,
        )
        await controller.send()

    @role.command(name="and-mention", description="指定した複数のロールをすべて持っているメンバーをメンションします。")
    async def and_mention(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        if interaction.channel is None or not issubclass(type(interaction.channel), discord.abc.Messageable):
            await interaction.followup.send("このコマンドはメッセージ可能なチャンネルでのみ実行できます。", ephemeral=True)
            return
        # channelはMessagableであることが保証されている
        channel: discord.abc.Messageable = interaction.channel  # type: ignore[assignment]

        controller = InteractionController(
            AndMentionView(),
            interaction=interaction,
            timeout=None,
            ephemeral=True,
        )
        await controller.send()
        _, states = await controller.wait()
        # states["selected"]は通常長さ1～5のlist[Role]であることが期待される
        # 長さが1だったら普通のメンションでいいので断る
        selected: list[discord.Role] = (
            r if isinstance(r := states.get("selected", []), list) and len(r) > 1 and isinstance(r[0], discord.Role) else []
        )
        if selected == []:
            await interaction.followup.send(
                "ロールが2つ以上選択されなかったため、処理を中断しました。メンション先ロールが1つであれば通常のメンションを利用してください。",
                ephemeral=True,
            )

        # 人数が小さい順にsort
        sorted_roles = sorted(selected, key=lambda r: len(r.members))
        # popすると人数が最も多いロールが取得できる
        biggest = sorted_roles.pop()
        # 人数が最も多いRoleのMemberから、残りのRoleをすべて持っているMemberのIDを抽出
        target_members: list[int] = await filter_users_by_roles(biggest.members, [r.id for r in sorted_roles])
        target_mentions = [f"<@{m}>" for m in target_members]

        # メンション文字列を2000文字以下ごとに分割して送信
        for string in chunk_str_iter_with_max_length(
            target_mentions, max_length=2000, separator="\n", ignore_oversize_fragment=True
        ):
            await channel.send(content=string)
            await asyncio.sleep(1)

        # メンション完了 :igyo:
        await channel.send(
            embed=Embed(
                title="一括メンション",
                description="""
このメンションは`/role and-mention`コマンドによって送信されました。
メンションの理由などは送信者にお問い合わせください。""",
                color=Color.MIKU,
            ).add_field(
                name="送信者",
                value=f"<@{interaction.user.id}>",
            )
        )
        return


async def filter_users_by_roles(users: list[Member], target_roles: list[int]) -> list[int]:
    # ユーザーごとのRoleセットを保持する辞書を作成
    user_roles_dict = {user.id: [role.id for role in user.roles] for user in users}

    # 指定されたRoleを持つUserを抽出
    return [
        user_id for user_id, user_roles in user_roles_dict.items() if all(role_id in user_roles for role_id in target_roles)
    ]


async def setup(bot: "Bot") -> None:
    await bot.add_cog(Role(bot))
