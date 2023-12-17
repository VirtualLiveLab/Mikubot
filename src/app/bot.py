import asyncio
import os

import discord

# import sentry_sdk
from discord.ext import commands

from src.app.core.chat.view import DispandView
from src.app.utils.view import DeleteView
from src.const.log import command_log, login_log
from src.utils.cog import CogLoader
from src.utils.finder import Finder
from src.utils.logger import get_my_logger

from .embed import ready_embed
from .tree import BotCommandTree

if not __debug__:
    from dotenv import load_dotenv

    load_dotenv()


class Bot(commands.Bot):
    def __init__(self) -> None:
        # self.init_sentry()
        self.config = {"prefix": "!"}
        self.logger = get_my_logger(__name__, level="DEBUG")

        # failed extension list
        self.failed_exts: list[str] = []
        self.failed_views: list[str] = []

        # set local application command sync target
        self.local_app_cmd_sync_target = discord.Object(int(os.environ["GUILD_ID"]))

        # set intents
        intents = discord.Intents.all()
        intents.typing = False
        intents.presences = False

        super().__init__(
            command_prefix=self.config.get("prefix", "!"),
            intents=intents,
            tree_cls=BotCommandTree,
        )

    async def setup_hook(self) -> None:
        await self.set_pre_invoke_hook()
        await self.load_exts()
        await self.sync_app_commands()
        await self.setup_views()

    async def on_ready(self) -> None:
        self.logger.info(login_log(user=self.user, guild_amount=len(self.guilds)))
        channel = await Finder(self).find_channel(int(os.environ["LOG_CHANNEL_ID"]), expected_type=discord.TextChannel)
        emb = ready_embed(
            latency=self.latency,
            failed_exts=self.failed_exts,
            failed_views=self.failed_views,
        )
        await channel.send(embed=emb)
        await self.change_presence(activity=discord.CustomActivity(name="ハウトゥー世界征服"))
        # await self.change_presence(activity=discord.Game(name="プロセカ"))

    async def load_exts(self) -> None:
        # load cogs automatically
        # "cog.py" under the "app" directory will loaded
        loader = CogLoader("src/app")
        cogs = loader.glob_cog("cog.py", as_relative=True)

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

    async def sync_app_commands(self) -> None:
        try:
            # execute global sync
            synced = await self.tree.sync(guild=None)
            # execute guild sync
            if self.local_app_cmd_sync_target is not None:
                local_synced = await self.tree.sync(guild=self.local_app_cmd_sync_target)
            else:
                local_synced = None
        except Exception:
            self.logger.exception("Failed to sync application commands")
        else:
            msg = f"{len(synced)} Application commands synced successfully"
            if local_synced is not None:
                msg += f"\n{len(local_synced)} Local application commands synced successfully (Guild: {self.local_app_cmd_sync_target.id})"  # noqa: E501
            self.logger.info(msg)

    async def setup_views(self) -> None:
        # NOTICE: message_url is only for LinkButton
        # This parameter is not used after once sended
        # So, this is dummy value
        self.add_view(DeleteView())
        self.add_view(DispandView(message_url="MISSING"))

    async def set_pre_invoke_hook(self) -> None:
        @self.before_invoke
        async def write_debug_log(ctx: commands.Context) -> None:
            self.logger.debug(command_log(ctx))

    # def init_sentry(self) -> None:
    #     sentry_sdk.init(
    #         dsn=os.environ["SENTRY_DSN"],
    #         # Set traces_sample_rate to 1.0 to capture 100%
    #         # of transactions for performance monitoring.
    #         # We recommend adjusting this value in production.
    #         traces_sample_rate=1.0,
    #     )

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
        import sys

        # from sentry_sdk import Hub
        # # shutdown Sentry
        # client = Hub.current.client
        # if client is not None:
        #     client.close(timeout=2.0)

        await self.close()
        sys.exit(status)
