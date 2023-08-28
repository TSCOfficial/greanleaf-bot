import discord
from discord.ext import commands
from discord.utils import get
from discord.app_commands import AppCommandError, CommandNotFound, MissingPermissions, Choice
from discord import app_commands

import config as config
from config import conf


class settings(commands.GroupCog, name="einstellung"):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(name="übersicht", description="Übersicht der aktuellen einstellungen")
    async def overview(self, interaction: discord.Interaction):
        embed = await conf().EMBED(
            interaction=interaction,
            title="Einstellungen",
            description="Sämtliche Server und Bot Einstellungen ansehen und bearbeiten.",
        )
        embed.add_field(name="Auto Thread", value="Thread Einstellungen ändern.\ncmd", inline=False)
        embed.add_field(name="Loggin", value="Log Einstellungen ändern.\ncmd", inline=False)
        embed.add_field(name="URL/Link Filter", value="Filter Einstellungen ändern.\ncmd", inline=False)
        embed.add_field(name="Support System", value="Support Einstellungen ändern."
                        "- Ticket System"
                        "- Support Talk Benachrichtigung", inline=False)
        await interaction.response.send_message(embed=embed)
        return


async def setup(client):
    await client.add_cog(settings(client))
    print(__name__)