import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from discord.utils import get
from discord.app_commands import AppCommandError, CommandNotFound, MissingPermissions
from datetime import datetime
import inspect

import config as config
from config import conf

class bot_info(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name="bot", description="Bot Informationen")
    async def bot(self, interaction:discord.Interaction):
        await interaction.response.defer()
        embed = await conf().EMBED(
            interaction=interaction,
            title=interaction.client.user.name,
            thumbnail_url=interaction.client.user.display_avatar,
            request=True
            )
        embed.add_field(name="Prefix", value="`g.` & App Befehle")
        embed.add_field(name="Entwicklerin", value=config.USER_ME_MENTION)
        embed.add_field(name="Server", value=len(interaction.client.guilds))
        embed.add_field(name="Verwendung", value="#Utility #Moderation #Logging", inline=False)
        embed.add_field(name="Seit", value="22.08.2023")
        await interaction.followup.send(embed=embed)
        return
        
async def setup(client):
    await client.add_cog(bot_info(client))
    print(__name__)
