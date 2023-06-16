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
    async def Balance(
        self,
        interaction: discord.Interaction,
    ):
        """Connect to DB and add urself as user"""
        db = await aiosqlite.connect("mydatabase.db")

        # Execute a SQL query to create a table
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE,
                username TEXT,
                beans INTEGER)"""
        )

        data = (interaction.user.id, interaction.user.name, 5)

        # Execute multiple SQL queries to insert data
        insert_query = "INSERT INTO users (user_id, username, beans) VALUES (?, ?, ?)"
        find_query = f"SELECT user_id FROM users WHERE user_id = {interaction.user.id}"
        try:
            await db.execute(insert_query, data)
            await db.commit()
            db.execute(find_query)
            results = db.fetchall()
            print(results)
            await interaction.response.send_message("Added to database")
        except Exception as e:
            print(e)
            await interaction.response.send_message(e)
        await db.close()

    @app_commands.command()
    async def table(
        self,
        interaction: discord.Interaction,
    ):
        """Show table details"""
        db = await aiosqlite.connect("mydatabase.db")

        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()

        # Print the table details
        if not rows:
            print(f"Table 'users' not found")

        # Close the cursor and the database connection
        await cursor.close()
        await db.close()
        await interaction.response.send_message(rows)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Balance(bot))
