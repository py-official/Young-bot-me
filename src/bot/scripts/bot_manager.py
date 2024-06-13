# python lib
from time import time
from logging import INFO

# pip lib
import disnake
from disnake.ext import commands
from disnake.ext.commands import Context, errors
from dotenv import dotenv_values

# project lib
from ..components.log.logger import CustomLogger

# creating logger
logger = CustomLogger(__name__, INFO)


class MEBot(commands.Bot):
    def __init__(self, name: str, cfg: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = time()
        self.name = name
        self.cfg = cfg
        self.log = Logger(name=self.name, file_name=self.name)

    def __repr__(self):
        return self.name

    async def on_ready(self):
        end_time = time()

        logger.info(self.cfg["replics"]["start"].format(user=self.user, during_time=end_time-self.start_time))

    async def on_command_error(self, context: Context, exception: errors.CommandError) -> None:
        logger.info("[&] Ignoring command -> %s" % context.message.content, log_text=False)


class BotManager():
    def __init__(self):
        self.cfg = JsonManager()
        self.log = Logger(name="Bot manager", file_name="bot_manager")
        self.cfg.dload_cfg(short_name="bots_properties.json")
        self.env_val = dotenv_values("data/sys/.env")
        self.BotsCont = {}
        logger.info("[&] Successful initialization of Bot manager")

    @staticmethod
    def init_assistant(func):
        def wrapper(self, name_bot):
            func(self, name_bot=name_bot, command_prefix=self.cfg.buffer[name_bot]["command_prefix"])

        return wrapper


    @init_assistant
    def init_bot(self, name_bot, **kwargs):
        logger.info(f"[&] Start to initialize a bot \"{name_bot}\"")
        intents = disnake.Intents.all()
        self.BotsCont[name_bot] = MEBot(name=name_bot, cfg=self.cfg.buffer[name_bot], intents=intents, **kwargs)

        for cog in self.cfg.buffer[name_bot]["cogs"]:
            logger.info(f"[&] Import \"{cog}\" to bot \"{name_bot}\"")
            self.BotsCont[name_bot].load_extension(cog)

        token = self.env_val[f"{name_bot}_TOKEN"]
        logger.info(f"[&] Successful initialization of bot \"{name_bot}\"")
        logger.info(f"[&] Starting bot \"{name_bot}\"")
        self.BotsCont[name_bot].run(token)
