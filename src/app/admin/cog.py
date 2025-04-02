from typing import TYPE_CHECKING

import discord
from discord import Interaction, app_commands
from discord.ext import commands

from .view import AdminUserInfoView, user_info_view_embed

if TYPE_CHECKING:
    # import some original class
    from src.app.bot import Bot


class Admin(commands.Cog):
    admin_group = app_commands.Group(name="admin", description="管理者向けのコマンド", guild_only=True)

    def __init__(self, bot: "Bot") -> None:
        self.bot = bot

    @admin_group.command(
        name="send-confirm-id-before-join-form",
        description="入部申請フォーム記入時に必要な ID を引くためのメッセージを送信します",
    )
    @app_commands.rename(
        target="送信先チャンネル",
    )
    @app_commands.describe(
        target="メッセージを送信するチャンネル",
    )
    async def send_confirm_id_before_join_form(self, interaction: "Interaction", target: discord.TextChannel) -> None:
        await interaction.response.defer(ephemeral=True)

        if not interaction.permissions.administrator:
            await interaction.followup.send(
                content="このコマンドは管理者のみが実行できます。",
                ephemeral=True,
            )
            return

        sent = await target.send(
            embed=user_info_view_embed(),
            view=AdminUserInfoView(),
        )

        await interaction.followup.send(
            content=(f"{target.mention} にメッセージを送信しました。\n[送信されたメッセージを見る]({sent.jump_url})"),
            ephemeral=True,
        )


async def setup(bot: "Bot") -> None:
    await bot.add_cog(Admin(bot))
