# ライブラリのインポート
from pprint import pprint
import discord
from discord.ext import commands
import requests

# おまじない(Botの用意)
bot = commands.Bot(command_prefix="!")
TOKEN = "TOKEN"  # EnterToken
webhook = "WEBHOOK"  # EnterWebhook


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    url = "https://discord.com/api/v8/channels/{0}/messages/{1}".format(message.channel.id, message.id)
    headers = {"Authorization": "Bot " + TOKEN}  # Practice
    mesjson = requests.get(url, headers=headers).json()
    picurl = mesjson["attachments"][0]["proxy_url"]
    requests.post(webhook, json={"content": picurl})
    await message.channel.send("done")


bot.run(TOKEN)
