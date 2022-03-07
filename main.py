import discord
import SQLite as SQL
from discord.ext import commands, tasks
from dislash import InteractionClient, slash_commands, Option, OptionType
from pprint import pprint
from datetime import datetime
import timetree as TT
import Keys as K
import urllib.request
from bs4 import BeautifulSoup

# コマンドが使えるようにするサーバーのIDを列挙
guilds = [938738282710335559]
Intents = discord.Intents.all()
client = commands.Bot(command_prefix='/', intents=Intents)
slash = slash_commands.SlashClient(client)
# inter_client = InteractionClient(client)

weatherURL = 'https://rss-weather.yahoo.co.jp/rss/days/13.xml'
tenki = []

async def weatherParser(rssurl):
   with urllib.request.urlopen(rssurl) as res:
      xml = res.read()
      soup = BeautifulSoup(xml, "html.parser")
      for item in soup.find_all("item"):
         title = item.find("title").string
         if title.find("[ PR ]") == -1:
            tenki.append(title)

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


@slash.command(name='wether', description='今日の天気は...', guild_ids=guilds)
async def wether(inter):
    await weatherParser(weatherURL)
    tenki_text = tenki[0][:-14]
    embed = discord.Embed(title='今日の天気は...', description=tenki_text, color=0x8affff)
    tenki.clear()
    await inter.reply(embed=embed)


loop.start()
client.run(K.RetKEY("VLL2022TOKEN"))
