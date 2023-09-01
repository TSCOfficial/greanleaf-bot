import discord
from discord.ext import commands
from discord import app_commands

import config as config
from config import conf

async def get_filter_overview(interaction: discord.Interaction):
    embed = await conf().EMBED(
        interaction=interaction,
        title="Filter",
        description="Bearbeite die Filter EInstellungen des Servers.",
    )
    return embed

class filter(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="filter", description="Filter Einstellungen ändern.")
    async def filter(self, interaction:discord.Interaction):
        await interaction.response.defer()
        await get_filter_overview(interaction)
        return

async def setup(bot):
    await bot.add_cog(filter(bot))
    print(__name__)