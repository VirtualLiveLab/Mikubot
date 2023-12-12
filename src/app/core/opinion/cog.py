import os
from traceback import print_exc

import discord
from discord import Embed, app_commands
from discord.ext import commands

from src.const.enums import Color
from src.utils.finder import Finder

from .view import OpinionModal


class Opinion(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="opinion", description="サークル運営についての意見を送信するよ！")
    @app_commands.guilds(discord.Object(id=int(os.environ["GUILD_ID"])))
    @app_commands.guild_only()
    async def opinion(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(OpinionModal(self.on_submit))

    async def on_submit(self, interaction: discord.Interaction, values: dict[str, str]) -> None:
        await interaction.response.defer(ephemeral=True)
        opinion = values.get("意見", "")

        try:
            embed = Embed(
                title="意見が届きました！",
                description=opinion,
                color=Color.MIKU,
            )
            # replace 0 with channel id
            finder = Finder(self.bot)
            channel = await finder.find_channel(int(os.environ["OPINION_CHANNEL_ID"]), expected_type=discord.Thread)
            await channel.send(embed=embed)
        except Exception:  # noqa: BLE001
            print_exc()
            e = Embed(
                title="エラーが発生しました。",
                description="送信に失敗しました。\n何度も続く場合は管理者に連絡してください。",
                color=Color.MIKU,
            )
        else:
            e = Embed(title="送信完了！", description="貴重なご意見ありがとうございます！", color=Color.MIKU)

        await interaction.edit_original_response(embed=e)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Opinion(bot))
