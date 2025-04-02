from typing import TYPE_CHECKING

from discord import AllowedMentions, Interaction, Member, app_commands
from discord.ext import commands

from .view import UserIdCopyView, user_embed

if TYPE_CHECKING:
    # import some original class
    from src.app.bot import Bot


class User(commands.Cog):
    user_group = app_commands.Group(name="user", description="ユーザー関連のコマンド")

    def __init__(self, bot: "Bot") -> None:
        self.bot = bot

    @user_group.command(name="me", description="自分の情報を表示します。入部時に必要です。")
    @app_commands.guild_only()
    async def me(self, interaction: "Interaction") -> None:
        await interaction.response.defer(ephemeral=True)

        embed = user_embed(interaction.user)
        await interaction.followup.send(
            embed=embed,
            view=UserIdCopyView(bound_user=interaction.user),
            allowed_mentions=AllowedMentions.none(),  # 不要なメンションを避ける
            ephemeral=True,
        )

    @user_group.command(name="fetch", description="ユーザーの情報を検索します。")
    @app_commands.rename(user="ユーザー")
    @app_commands.describe(user="検索するユーザー。補完に出なくても固有 ID を入力すれば検索できます。")
    async def fetch(self, interaction: "Interaction", user: "Member") -> None:
        await interaction.response.defer(ephemeral=True)

        embed = user_embed(user)
        await interaction.followup.send(
            embed=embed,
            view=UserIdCopyView(bound_user=user),
            allowed_mentions=AllowedMentions.none(),  # 不要なメンションを避ける
            ephemeral=True,
        )


async def setup(bot: "Bot") -> None:
    await bot.add_cog(User(bot))
