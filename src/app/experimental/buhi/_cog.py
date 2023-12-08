import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from src.components.status import StatusUI
from src.const.enums import Color, Role, Status
from src.utils.validator import validate

if TYPE_CHECKING:
    # import some original class
    from src.app.bot import Bot


class RoleError(Exception):
    pass


class Buhi(commands.Cog):
    def __init__(self, bot: "Bot") -> None:
        self.bot = bot

    group = app_commands.Group(
        name="buhi",
        description="部費ロール管理",
        guild_ids=[int(os.environ["GUILD_ID"])],
    )

    # NOTICE: DiscordのOnboarding機能に移行しない場合コメントアウトを外す
    # @commands.Cog.listener("on_member_join")
    # async def add_minou_role_automatically(self, member: discord.Member):
    #     await self.add_minou_role(member)
    #     return

    @group.command(name="add", description="部費未納ロールを付与します")  # type: ignore[arg-type]
    @app_commands.guild_only()
    async def add_minou_role_command(self, interaction: discord.Interaction, member: discord.Member) -> None:
        await interaction.response.defer()
        author = validate(interaction.user, discord.Member)
        ui = StatusUI(color=Color.MIKU)

        if not self.check_kaikei_role(author):
            ui.add(
                key="FAILED",
                status=Status.FAILED,
                message="このコマンドを実行する権限がありません。",
            )
            ui.color = Color.WARNING
            await ui.send(interaction.followup)
            return

        ui.add(
            key="ROLE_STATUS",
            status=Status.IN_PROGRESS,
            message=f"{member.mention}に部費未納ロールを付与しています...",
        )
        await ui.send(interaction.followup)

        try:
            await self.add_minou_role(member)
        except Exception as e:
            self.bot.logger.exception("部費未納ロールの付与に失敗しました。")
            ui.update(
                key="ROLE_STATUS",
                status=Status.FAILED,
                message=f"{member.mention}に部費未納ロールを付与できませんでした。",
            )
            ui.color = Color.WARNING
            ui._dangerously_edit_embed(  # noqa: SLF001
                lambda em, d: em.add_field(name="エラー内容", value=f"```\n{d['error']}\n```"),
                kwargs={"error": e},
            )
            await ui.sync()
        else:
            ui.update(
                key="ROLE_STATUS",
                status=Status.SUCCESS,
                message=f"{member.mention}に部費未納ロールを付与しました！",
            )
            ui.color = Color.SUCCESS
            await ui.sync()
        return

    @group.command(name="remove", description="部費未納ロールを消去します")  # type: ignore[arg-type]
    @app_commands.guild_only()
    async def remove_minou_role_command(self, interaction: discord.Interaction, member: discord.Member) -> None:
        await interaction.response.defer()
        author = validate(interaction.user, discord.Member)

        ui = StatusUI(color=Color.MIKU)
        if not self.check_kaikei_role(author):
            ui.add(key="FAILED", status=Status.FAILED, message="このコマンドを実行する権限がありません。")
            ui.color = Color.WARNING
            await ui.send(interaction.followup)
            return

        ui.add(
            key="ROLE_STATUS",
            status=Status.IN_PROGRESS,
            message=f"{member.mention}から部費未納ロールを消去しています...",
        )
        await ui.send(interaction.followup)

        try:
            await self.remove_minou_role(member)
        except Exception as e:
            self.bot.logger.exception("部費未納ロールの消去に失敗しました。")
            ui.update(
                key="ROLE_STATUS",
                status=Status.FAILED,
                message=f"{member.mention}から部費未納ロールを消去できませんでした。",
            )
            ui.color = Color.WARNING
            ui._dangerously_edit_embed(  # noqa: SLF001
                lambda em, d: em.add_field(name="エラー内容", value=f"```\n{d['error']}\n```"),
                kwargs={"error": e},
            )
            await ui.sync()
        else:
            ui.update(
                key="ROLE_STATUS",
                status=Status.SUCCESS,
                message=f"{member.mention}から部費未納ロールを消去しました！",
            )
            ui.color = Color.SUCCESS
            await ui.sync()
        return

    async def add_minou_role(self, member: discord.Member) -> None:
        if Role.BUHI_MINOU in [r.id for r in member.roles]:
            msg = f"{member.mention}には既に部費未納ロールが付与されています。"
            raise RoleError(msg)
        await member.add_roles(discord.Object(id=Role.BUHI_MINOU))

    async def remove_minou_role(self, member: discord.Member) -> None:
        if Role.BUHI_MINOU not in [r.id for r in member.roles]:
            msg = f"{member.mention}には部費未納ロールが付与されていません。"
            raise RoleError(msg)
        await member.remove_roles(discord.Object(id=Role.BUHI_MINOU))

    def check_kaikei_role(self, member: discord.Member) -> bool:
        return Role.KAIKEI in [r.id for r in member.roles]


async def setup(bot: "Bot") -> None:
    await bot.add_cog(Buhi(bot))
