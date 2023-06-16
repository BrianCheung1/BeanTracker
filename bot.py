import discord
import os
import platform
import asyncio
import aiosqlite
from dotenv import load_dotenv
from discord.ext.commands import Bot
from discord.ext import commands


load_dotenv()

MY_GUILD = discord.Object(id=152954629993398272)


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="`",
            intents=discord.Intents.all(),
            help_command=None,
        )

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        # if os.getenv("SYNC") is True:
        #     print("Syncing commands globally...")
        #     await bot.tree.sync()
        # else:
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


bot = MyBot()
token = os.getenv("TOKEN")


@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user}")
    print(f"Running discord.py API version {discord.__version__}")
    print(f"Running python verison {platform.python_version}")


async def load_cogs() -> None:
    for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")

async def load_db():
    async with aiosqlite.connect('users.db') as db:
        with open(f"{os.path.realpath(os.path.dirname(__file__))}/database/schema.sql") as file:
            print(file.read())
            await db.executescript(file.read())
        await db.commit()

asyncio.run(load_db())
asyncio.run(load_cogs())
bot.run(token)
