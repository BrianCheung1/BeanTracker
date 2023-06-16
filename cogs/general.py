import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


# Here we name the cog and create a new class for the cog.
class Template(commands.Cog, name="General"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def hello(self, interaction: discord.Interaction):
        """Says hello!"""
        await interaction.response.send_message(f"Hi, {interaction.user.mention}")

    @app_commands.command()
    @app_commands.describe()
    async def reload(self, interaction: discord.Interaction):
        """Adds two numbers together"""
        await self.bot.reload_extension("cogs.general")
        await self.bot.reload_extension("cogs.balance")
        await interaction.response.send_message("reloaded")


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Template(bot))
