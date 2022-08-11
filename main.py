import discord
import SQLite as SQL
from discord.ext import commands, tasks
from dislash import InteractionClient, slash_commands, Option, OptionType, ActionRow, Button, ButtonStyle
from pprint import pprint
from datetime import datetime
import timetree as TT
import os

# コマンドが使えるようにするサーバーのIDを列挙
guilds = [938738282710335559]
Intents = discord.Intents.all()
client = commands.Bot(command_prefix='/', intents=Intents)
slash = slash_commands.SlashClient(client)
# inter_client = InteractionClient(client)
    

@client.event
async def on_ready():
    print('Done Login')
    ch_id = 938738283364618264  # general
    chennel = client.get_channel(ch_id)
    embed = discord.Embed(description="ミクが起動したよ!", color=0x66DDCC)
    await chennel.send(embed=embed)
    await client.change_presence(activity=discord.Game('プロセカ'))


@tasks.loop(minutes=1)
async def loop():
    channel = client.get_channel(941312720492433449)
    now = datetime.now().strftime('%H:%M')
    if now == '08:39':
        await channel.send(embed=TT.getTodaysEvents('おはミク!!'))


@client.event
async def on_raw_reaction_add(payload):
    if payload.emoji.id != 939218534515494932:
        return
    print(payload.message_id)
    willAddRoleId = SQL.out(payload.message_id)
    if willAddRoleId == -1:
        return

    guild_id = payload.guild_id
    guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
    role = guild.get_role(willAddRoleId)
    await payload.member.add_roles(role)


@client.event
async def on_raw_reaction_remove(payload):
    if payload.emoji.id != 939218534515494932:
        return
    willAddRoleId = SQL.out(payload.message_id)
    if willAddRoleId == -1:
        return

    guild_id = payload.guild_id
    guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
    role = guild.get_role(willAddRoleId)
    member = guild.get_member(payload.user_id)
    await member.remove_roles(role)


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content == 'miku':
        await message.channel.send('MIKU!')
    elif 'うおうお' in message.content:
        await message.add_reaction('\N{FISH}')
    elif 'ふろ' in message.content:
        await message.add_reaction('\N{bathtub}')
    elif 'Docker' in message.content:
        await message.add_reaction('\N{whale}')
    elif 'ミクさん！' == message.content:
        await message.channel.send('呼んだ？')


@client.event
async def on_member_join(member):
    role_buhi = discord.utils.get(member.guild.roles, id=938738282894852100)
    await member.add_roles(role_buhi)


@slash.command(name='timetree', description='今日の予定をとってくるよ', guild_ids=guilds)
async def timetree(inter):
    inter_ = inter
    json = TT.getTodaysEventsJson('ミクミク!')
    # pprint(json)
    await inter_.reply(embed=json)


@slash.command(name='miku', description='ミクさんが返事をしてくれるよ', guild_ids=guilds)
async def miku(inter):
    await inter.reply("MIKU!!!")


@slash.command(name='helloworld', description='Hello world!', guild_ids=guilds)
async def helloworld(inter):
    inter_ = inter
    user = inter_.author
    emb = discord.Embed(color=discord.Color.blurple())
    emb.title = str(user)
    emb.description = (
        f"**Created at:** `{user.created_at}`\n"
        f"**ID:** `{user.id}`"
    )
    emb.set_thumbnail(url=user.avatar_url)
    await inter_.respond(embed=emb)


@slash.command(name='addlist', description='データベースに情報を追加するよ!', options=[
    Option('text_id', '変換元のテキストid', OptionType.STRING, required=True),
    Option('role_id', '変換先のロールid', OptionType.STRING, required=True),
], guild_ids=guilds)
async def addid(inter, text_id, role_id):
    inter_ = inter
    guild_id = inter_.guild_id
    guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
    admin = guild.get_role(938738282894852105)
    user = inter_.author
    if admin in user.roles:
        SQL.set_id(text_id, role_id)
        embed = SQL.makeDBembed()
        await inter_.reply(embed=embed)

    else:
        embed = discord.Embed(description="You have no permission", color=0xFF0000)
        await inter_.reply(embed=embed)


@slash.command(name='list', description='データベースを確認するよ!', guild_ids=guilds)
async def list(inter):
    inter_ = inter
    guild_id = inter_.guild_id
    guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
    admin = guild.get_role(938738282894852105)
    user = inter_.author
    if admin in user.roles:
        embed = SQL.makeDBembed()
        await inter_.reply(embed=embed)

    else:
        embed = discord.Embed(description="You have no permission", color=0xFF0000)
        await inter_.reply(embed=embed)


@slash.command(name='delid', description='データベースから情報を削除するよ!', options=[
    Option('id', '変換元の固有id(一つ目の値)', OptionType.INTEGER, required=True)
], guild_ids=guilds)
async def delid(inter, id):
    inter_ = inter
    guild_id = inter_.guild_id
    guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
    admin = guild.get_role(938738282894852105)
    user = inter_.author
    if admin in user.roles:
        SQL.del_id(id)
        embed = SQL.makeDBembed()
        await inter_.reply(embed=embed)

    else:
        embed = discord.Embed(description="You have no permission", color=0xFF0000)
        await inter.reply(embed=embed)


@slash.command(name='miku', description='ミクさんが返事をしてくれるよ', guild_ids=guilds)
async def miku(inter):
    await inter.reply("MIKU!!!")


@slash.command(name='vote', description='vote', guild_ids=guilds)
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
    msg = await ctx.send("投票", components=[row])
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
        embed.set_author(name=ctx.author,
                         icon_url=ctx.author.avatar_url  # Botのアイコンを設定してみる
                         )
        embed.add_field(name="A", value=str(len(A)))
        embed.add_field(name="B", value=str(len(B)))

        await ctx.send(embed=embed)
        await msg.edit(components=[])


@slash.command(name='vote_name', description='vote add name', guild_ids=guilds)
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
    msg = await ctx.send("投票", components=[row])
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
        embed.set_author(name=ctx.author,
                         icon_url=ctx.author.avatar_url  # Botのアイコンを設定してみる
                         )
        embed.add_field(name="A", value=str(len(A)) + "\n" + "\n".join(A))
        embed.add_field(name="B", value=str(len(B)) + "\n" + "\n".join(B))

        await ctx.send(embed=embed)
        await msg.edit(components=[])


@slash.command(name='kaikei', guild_ids=guilds)
async def kaikei(inter):
    pass


@kaikei.sub_command(description="remove role", options=[
    Option('user', "remove", OptionType.USER, required=True)
])
async def remove(inter, user):
    inter_ = inter
    count = 0
    for x in inter.author.roles:
        if x.id == 938738282894852103:
            count = 1

    if count == 1:
        try:
            guild_id = inter_.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
            role = guild.get_role(938738282894852100)
            embed = discord.Embed(title="success!", description="remove role from " + user.name, color=0x00ff00)
            await user.remove_roles(role)
            await inter_.reply(embed=embed)

        except:
            embed = discord.Embed(title="error!", description="Not found Role!", color=0xff0000)
            await inter_.reply(embed=embed)

    if count == 0:
        embed = discord.Embed(title="error!", description="you don't have permission!", color=0xff0000)
        await inter_.reply(embed=embed)


@kaikei.sub_command(description="add role", options=[
    Option('user', "add", OptionType.USER, required=True)
])
async def add(inter, user):
    inter_ = inter
    count = 0
    for x in inter.author.roles:
        if x.id == 938738282894852103:
            count = 1

    if count == 1:
        try:
            guild_id = inter_.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
            role = guild.get_role(938738282894852100)
            embed = discord.Embed(title="success!", description="add role " + user.name, color=0x00ff00)
            await user.add_roles(role)
            await inter_.reply(embed=embed)

        except:
            embed = discord.Embed(title="error!", description="Error!", color=0xff0000)
            await inter_.reply(embed=embed)

    if count == 0:
        embed = discord.Embed(title="error!", description="you don't have permission!", color=0xff0000)
        await inter_.reply(embed=embed)


loop.start()
client.run(os.getenv('token'))
