import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import aiosqlite


# Here we name the cog and create a new class for the cog.
class Balance(commands.Cog, name="Balance"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def balance(
        self,
        interaction: discord.Interaction,
    ):
        """Connect to DB and add urself as user"""

        async with aiosqlite.connect("users.db") as db:
            async with db.execute("SELECT * FROM users WHERE user_id =?", (interaction.user.id,)) as cursor:
                result = await cursor.fetchone()
                if not result:
                    await db.execute("INSERT INTO users (user_id, username, beans) VALUES(?,?,?)", (interaction.user.id, interaction.user.name, 5))
                    await db.commit()
                    print("added to database")
                    result = await cursor.fetchone()
                try:
                    print(result)
                    await interaction.response.send_message(result)
                except Exception as e:
                    print(e)
                    await interaction.response.send_message(e)


    @app_commands.command()
    async def add_bean(
        self,
        interaction: discord.Interaction,
    ):
        """add a bean to a user"""
        async with aiosqlite.connect("users.db") as db:
            async with db.execute("SELECT * FROM users WHERE user_id =?", (interaction.user.id,)) as cursor:
                result = await cursor.fetchone()
                if not result:
                    insert_query = ("INSERT INTO users (user_id, username, beans) VALUES(?,?,?)", (interaction.user.id, interaction.user.name, 5))
                    await db.execute(insert_query)
                    await db.commit()
                    print("added to database")
                    result = await cursor.fetchone()
                try:
                    await db.execute("UPDATE users SET beans=beans+1 WHERE user_id =?", (interaction.user.id,))
                    await db.commit()
                    cursor = await db.execute("SELECT * FROM users WHERE user_id =?", (interaction.user.id,)) 
                    result = await cursor.fetchone()
                    print("updated database")
                    await interaction.response.send_message(result)
                except Exception as e:
                    print(e)
                    await interaction.response.send_message(e)



# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Balance(bot))
