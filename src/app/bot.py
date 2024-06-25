import asyncio
import os
import sys

import discord
import sentry_sdk

# import sentry_sdk
from discord.ext import commands
from sentry_sdk import Hub

from src.app.core.extract.view import DispandView
from src.app.utils.view import DeleteView
from src.config.intent import get_full_intents
from src.const.log import login_log
from src.utils.finder import Finder
from src.utils.logger import get_my_logger
from src.utils.path import PyPathFinder

from .embed import ready_embed
from .tree import BotCommandTree

if not __debug__:
    from dotenv import load_dotenv

    load_dotenv()


class Bot(commands.Bot):
    def __init__(self) -> None:
        self.init_sentry()
        self.config = {"prefix": "!"}
        self.logger = get_my_logger(__name__, level="DEBUG")

        # failed extension list
        self.failed_exts: list[str] = []
        self.failed_views: list[str] = []

        super().__init__(
            command_prefix=self.config.get("prefix", "!"),
            intents=get_full_intents(),
            tree_cls=BotCommandTree,
        )
        """
        tree_clsにBotCommandTreeを渡すことで、Application Command全般に追加操作を適用できる
        """

    async def setup_hook(self) -> None:
        await self.load_exts()
        await self.sync_app_commands()
        await self.setup_views()

    async def on_ready(self) -> None:
        self.logger.info(login_log(user=self.user, guild_amount=len(self.guilds)))
        channel = await Finder(self).find_channel(int(os.environ["LOG_CHANNEL_ID"]), expected_type=discord.Thread)
        emb = ready_embed(
            latency=self.latency,
            failed_exts=self.failed_exts,
            failed_views=self.failed_views,
        )
        await channel.send(embed=emb)
        await self.change_presence(activity=discord.CustomActivity(name="今年もよろしくねっ"))
        # await self.change_presence(activity=discord.Game(name="プロセカ"))

    async def load_exts(self) -> None:
        # load cogs automatically
        # "cog.py" under the "app" directory will loaded
        # cogs = [ "src.app.help.cog", ... ]
        path = PyPathFinder("src/app")
        cogs = path.glob_path("cog.py", as_relative=True)

        if cogs is None or cogs == []:
            return

        for cog in cogs:
            try:
                await self.load_extension(cog)
                msg = f"Loaded {cog}"
                self.logger.debug(msg)
            except Exception:
                msg = f"Failed to load {cog}"
                self.logger.exception(msg)
                self.failed_exts.append(cog)

    async def sync_app_commands(self) -> None:
        """
        Sync application commands. Must called after cog loaded.

        (If you called this before cog loaded, commands in cogs will not be synced)
        """
        try:
            # execute global sync
            # サーバー固有のコマンドは基本的に追加しない方針なので、guild=None
            synced = await self.tree.sync(guild=None)
        except Exception:
            self.logger.exception("Failed to sync application commands")
        else:
            msg = f"{len(synced)} Application commands synced successfully"
            self.logger.info(msg)

    async def setup_views(self) -> None:
        # NOTICE: message_url is only for LinkButton
        # This parameter is not used after once sended
        # So, this is dummy value
        views: list[discord.ui.View] = [
            DispandView(message_url="MISSING", button_label="MISSING"),
            DeleteView(),
        ]

        for v in views:
            try:
                self.add_view(v)
            except Exception:
                msg = f"Failed to setup {v}"
                self.logger.exception(msg)
                self.failed_views.append(str(v))

    def init_sentry(self) -> None:
        sentry_sdk.init(
            dsn=os.environ["SENTRY_DSN"],
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production.
            traces_sample_rate=0.75,
        )

    def runner(self, *, token: str) -> None:
        try:
            asyncio.run(self._runner(token=token))
        except ValueError:
            self.logger.exception("Failed to start bot")
            asyncio.run(self.shutdown(status=1))

    async def _runner(self, *, token: str) -> None:
        try:
            async with self:
                await self.start(token)
        except TypeError:
            self.logger.exception("Failed to start bot")
            await self.shutdown()

    async def shutdown(self, status: int = 0) -> None:
        # shutdown Sentry
        client = Hub.current.client
        if client is not None:
            client.close(timeout=2.0)

        await self.close()
        sys.exit(status)
