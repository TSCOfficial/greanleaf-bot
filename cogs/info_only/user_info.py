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

class user_info(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name="benutzer", description="enutzer Informationen")
    async def user(self, interaction:discord.Interaction):
        await interaction.response.defer()
        embed = await conf().EMBED(
            interaction=interaction,
            title=interaction.user.name,
            thumbnail_url=interaction.user.display_avatar,
            request=interaction.user
            )
        embed.add_field(name="Nickname", value=interaction.user.nick if interaction.user.nick else config.EMOJI_BOX_UNSET + "Nicht gesetzt")
        embed.add_field(name="Pomelo", value=config.EMOJI_HASH + "Ja" if interaction.user.discriminator == str(0) else config.EMOJI_HASH + f"Nein, #{interaction.user.discriminator}")
        embed.add_field(name="Nitro", value=config.EMOJI_ISPREMIUM + interaction.user.premium_since if interaction.user.premium_since is not None else config.EMOJI_NOTPREMIUM + "Kein Nitro")
        await interaction.followup.send(embed=embed)
        return
        
async def setup(client):
    await client.add_cog(user_info(client))
    print(__name__)
