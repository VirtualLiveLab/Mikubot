import asyncio
import secrets
from typing import TYPE_CHECKING, Literal, TypeAlias

import discord
from discord import app_commands
from discord.ext import commands

from .embed import omikuji_embed

if TYPE_CHECKING:
    # import some original class
    from src.app.bot import Bot


class Chat(commands.Cog):
    def __init__(self, bot: "Bot") -> None:
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def add_reaction_to_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        match message.content:
            case "miku":
                await message.channel.send("MIKU!")
            case "ミクさん！":
                await message.channel.send("呼んだ？")
            case "うおうお":
                await message.add_reaction("\N{FISH}")
            case "ふろ":
                await message.add_reaction("\N{BATHTUB}")
            case "Docker":
                await message.add_reaction("\N{WHALE}")
            case _:
                pass

    @app_commands.command(name="omikuji", description="おみくじを引くよ！")
    async def omikuji(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=False, thinking=True)
        result = get_omikuji_result()
        await asyncio.sleep(1)
        embed = omikuji_embed(result, OMKIJI_RESULT_DICT[result])
        await interaction.followup.send(embed=embed, ephemeral=False)

    @app_commands.command(name="miku", description="ミクさんが返事をしてくれるよ！")
    async def call_miku(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send("MIKU!")


OmikujiResult: TypeAlias = Literal["大吉", "中吉", "小吉", "吉", "末吉", "凶", "大凶"]
OMKIJI_RESULT_DICT: dict[OmikujiResult, str] = {
    "大吉": "大吉だよ！",
    "中吉": "中吉だよ！",
    "小吉": "小吉だよ！",
    "吉": "吉だよ！",
    "末吉": "末吉だよ！",
    "凶": "凶だよ！",
    "大凶": "大凶だよ！",
}


def get_omikuji_result() -> OmikujiResult:
    result: OmikujiResult = "大吉"
    rand = secrets.randbelow(6)
    match rand:
        case 0:
            result = "大吉"
        case 1:
            result = "中吉"
        case 2:
            result = "小吉"
        case 3:
            result = "吉"
        case 4:
            result = "末吉"
        case 5:
            result = "凶"
        case _:
            result = "大凶"

    return result


async def setup(bot: "Bot") -> None:
    await bot.add_cog(Chat(bot))
