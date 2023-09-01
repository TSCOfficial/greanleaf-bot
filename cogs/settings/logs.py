import discord
from discord.ext import commands
from discord import app_commands

import config as config
from config import conf

async def get_logs_overview(interaction: discord.Interaction):
    embed = await conf().EMBED(
        interaction=interaction,
        title="Logs",
        description="Bearbeite die Logs EInstellungen des Servers.",
    )
    return embed

class logs(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="logs", description="Log Einstellungen ändern.")
    async def log(self, interaction:discord.Interaction):
        await interaction.response.defer()
        await get_logs_overview(interaction)
        return
    
async def setup(bot):
    await bot.add_cog(logs(bot))
    print(__name__)