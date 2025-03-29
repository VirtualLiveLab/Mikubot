import discord


def user_embed(
    user: discord.Member | discord.User,
) -> discord.Embed:
    embed = discord.Embed(title=user.display_name, description=user.mention)
    embed.add_field(name="ユーザー名", value=user.display_name)
    embed.add_field(
        name="固有 ID",
        value=user.id,
    )
    if isinstance(user, discord.Member):
        owned_roles = [role for role in user.roles if role != user.guild.default_role]

        embed.add_field(
            name=f"所持ロール ({len(owned_roles)})",
            value="\n".join([role.mention for role in owned_roles]) if owned_roles != [] else "なし",
            inline=False,
        )

    embed.set_thumbnail(url=user.display_avatar.url)
    return embed


class UserEmbedView(discord.ui.View):
    def __init__(self, *, bound_user: discord.User | discord.Member) -> None:
        super().__init__(timeout=None)
        self.user = bound_user

    @discord.ui.button(
        label="固有 ID をコピーしたい(スマホ向け)", custom_id="user_view_copy_id", style=discord.ButtonStyle.secondary
    )
    async def on_click(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await interaction.response.send_message(
            content=self.user.id,
            ephemeral=True,
        )
