import discord
from discord.ext import commands
from discord.utils import get
from discord.app_commands import AppCommandError, CommandNotFound, MissingPermissions, Choice
from discord import app_commands

import config as config
from config import conf

async def get_autothread_overview(interaction: discord.Interaction):
    embed = await conf().EMBED(
        interaction=interaction,
        title="Auto Thread",
        description="Bearbeite die Auto Thread EInstellungen des Servers.",
    )
    embed.add_field(name="Auto Thread", value="Thread Einstellungen ändern.\ncmd", inline=False)
    return embed

class autothread(commands.GroupCog, name="thread"):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(name="übersicht", description="Übersicht der aktuellen Einstellungen")
    async def thread_overview(self, interaction: discord.Interaction):
        from cogs.settings.settingpage import goto_settinghome
        embed = await get_autothread_overview(interaction=interaction)
        await interaction.response.send_message(embed=embed, view=goto_settinghome())
        return
    
async def setup(client):
    await client.add_cog(autothread(client))
    print(__name__)