import discord
from discord.ext import commands
from discord.app_commands import AppCommandError, CommandNotFound, MissingPermissions, Choice
from discord import app_commands

class devpage(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="msg", description="Sende eine Nachricht")
    async def msg(self, interaction:discord.Interaction, nachricht:str):
        await interaction.response.send_message(content=nachricht)
        return

async def setup(bot):
    await bot.add_cog(devpage(bot))
    print(__name__)