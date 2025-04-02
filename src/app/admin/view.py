import discord

from src.app.user.view import UserIdCopyView


def user_info_view_embed() -> discord.Embed:
    return discord.Embed(
        title="入部申請時に必要なユーザー固有 ID について",
        description=(
            "ユーザー名を変更しても誰か分かるようにするために、入部時にユーザーごとの固有 ID を取得しています。\n"
            "このメッセージについているボタンから自分のものを確認できるので、申請フォームに記入をお願いします。"
        ),
    )


def user_id_embed(user: discord.Member | discord.User) -> discord.Embed:
    embed = discord.Embed()
    embed.add_field(name="ユーザー名", value=user.display_name)
    embed.add_field(
        name="固有 ID",
        value=user.id,
    )
    return embed


class AdminUserInfoView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(
        label="入部申請に必要な自分のユーザー情報を見る",
        style=discord.ButtonStyle.primary,
        custom_id="admin_user_info_view_get_user_information",
    )
    async def get_user_information(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await interaction.response.defer(ephemeral=True)

        user = interaction.user

        if not user:
            await interaction.followup.send(
                content="ユーザー情報が取得できませんでした。",
                ephemeral=True,
            )
            return

        embed = user_id_embed(user)
        await interaction.followup.send(
            embed=embed,
            view=UserIdCopyView(bound_user=interaction.user),
            allowed_mentions=discord.AllowedMentions.none(),  # 不要なメンションを避ける
            ephemeral=True,
        )
