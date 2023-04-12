from discord.ext import commands
import discord
from dislash import InteractionClient, ActionRow, Button, ButtonStyle
# import TOKEN
import os
from pprint import pprint

Intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=Intents)
inter_client = InteractionClient(bot)


@bot.command()
async def vote(ctx):
    row = ActionRow(
        Button(
            style=ButtonStyle.green,
            label="A",
            custom_id="A"
        ),
        Button(
            style=ButtonStyle.red,
            label="B",
            custom_id="B"
        )
    )
    msg = await ctx.send("UOUO!", components=[row])
    A = []
    B = []
    on_click = msg.create_click_listener(timeout=30)

    @on_click.matching_id("A")
    async def on_test_button(inter):
        if (str(inter.author.id) in A) or (str(inter.author.id) in B):
            await inter.reply("You are already voted!", ephemeral=True)

        else:
            A.append(str(inter.author.id))
            await inter.reply("You've voted A", ephemeral=True)

    @on_click.matching_id("B")
    async def on_test_button(inter):
        if (str(inter.author.id) in A) or (str(inter.author.id) in B):
            await inter.reply("You are already voted!", ephemeral=True)

        else:
            B.append(str(inter.author.id))
            await inter.reply("You've voted B", ephemeral=True)

    @on_click.timeout
    async def on_timeout():
        embed = discord.Embed(
            title="結果",
            color=0x00ff00,
        )
        embed.set_author(name=ctx.message.author,
                         icon_url=ctx.message.author.avatar_url  # Botのアイコンを設定してみる
                         )
        embed.add_field(name="A", value=str(len(A)))
        embed.add_field(name="B", value=str(len(B)))
        embed.set_footer(text="made by P4sTela",
                         icon_url="https://raw.githubusercontent.com/P4sTela/P4sTela/main/iconmono_500.png")

        await ctx.send(embed=embed)
        await msg.edit(components=[])


@bot.command()
async def vote_id(ctx):
    row = ActionRow(
        Button(
            style=ButtonStyle.green,
            label="A",
            custom_id="A"
        ),
        Button(
            style=ButtonStyle.red,
            label="B",
            custom_id="B"
        )
    )
    msg = await ctx.send("UOUO!", components=[row])
    A = []
    B = []
    on_click = msg.create_click_listener(timeout=30)

    @on_click.matching_id("A")
    async def on_test_button(inter):
        if (str(inter.author.id) in A) or (str(inter.author.id) in B):
            await inter.reply("You are already voted!", ephemeral=True)

        else:
            A.append(str(inter.author.id))
            await inter.reply("You've voted A", ephemeral=True)

    @on_click.matching_id("B")
    async def on_test_button(inter):
        if (str(inter.author.id) in A) or (str(inter.author.id) in B):
            await inter.reply("You are already voted!", ephemeral=True)

        else:
            B.append(str(inter.author.id))
            await inter.reply("You've voted B", ephemeral=True)

    @on_click.timeout
    async def on_timeout():
        embed = discord.Embed(
            title="結果",
            color=0x00ff00,
        )
        embed.set_author(name=ctx.message.author,
                         icon_url=ctx.message.author.avatar_url  # Botのアイコンを設定してみる
                         )
        embed.add_field(name="A", value=str(len(A)) + "\n" + "\n".join(A))
        embed.add_field(name="B", value=str(len(B)) + "\n" + "\n".join(B))
        embed.set_footer(text="made by P4sTela",
                         icon_url="https://raw.githubusercontent.com/P4sTela/P4sTela/main/iconmono_500.png")

        await ctx.send(embed=embed)
        await msg.edit(components=[])


@bot.command()
async def vote_name(ctx):
    row = ActionRow(
        Button(
            style=ButtonStyle.green,
            label="A",
            custom_id="A"
        ),
        Button(
            style=ButtonStyle.red,
            label="B",
            custom_id="B"
        )
    )
    msg = await ctx.send("UOUO!", components=[row])
    A = []
    B = []
    on_click = msg.create_click_listener(timeout=30)

    @on_click.matching_id("A")
    async def on_test_button(inter):
        if (str(inter.author.name) in A) or (str(inter.author.name) in B):
            await inter.reply("You are already voted!", ephemeral=True)

        else:
            A.append(str(inter.author.name))
            await inter.reply("You've voted A", ephemeral=True)

    @on_click.matching_id("B")
    async def on_test_button(inter):
        if (str(inter.author.name) in A) or (str(inter.author.name) in B):
            await inter.reply("You are already voted!", ephemeral=True)

        else:
            B.append(str(inter.author.name))
            await inter.reply("You've voted B", ephemeral=True)

    @on_click.timeout
    async def on_timeout():
        embed = discord.Embed(
            title="結果",
            color=0x00ff00,
        )
        embed.set_author(name=ctx.message.author,
                         icon_url=ctx.message.author.avatar_url  # Botのアイコンを設定してみる
                         )
        embed.add_field(name="A", value=str(len(A)) + "\n" + "\n".join(A))
        embed.add_field(name="B", value=str(len(B)) + "\n" + "\n".join(B))
        embed.set_footer(text="made by P4sTela",
                         icon_url="https://raw.githubusercontent.com/P4sTela/P4sTela/main/iconmono_500.png")

        await ctx.send(embed=embed)
        await msg.edit(components=[])


bot.run(os.getenv('token'))
