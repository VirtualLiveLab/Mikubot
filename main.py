from os import getenv

from src.app.bot import Bot

if __name__ == "__main__":
    token = getenv("DISCORD_BOT_TOKEN")
    if token is None:
        msg = "DISCORD_BOT_TOKEN is not found. Quitting..."
        raise ValueError(msg)

    bot = Bot()
    bot.runner(token=token)
