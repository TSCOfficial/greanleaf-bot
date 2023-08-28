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


async def get_userinfo(interaction):
    embed = await conf().EMBED(
        interaction=interaction,
        title=interaction.user.name,
        thumbnail_url=interaction.user.display_avatar,
        request=interaction.user
        )
    embed.add_field(name="Nickname", value=interaction.user.nick if interaction.user.nick else config.EMOJI_BOX_UNSET + "Nicht gesetzt")
    embed.add_field(name="Pomelo", value=config.EMOJI_HASH + "Ja" if interaction.user.discriminator == str(0) else config.EMOJI_HASH + f"Nein, #{interaction.user.discriminator}")
    embed.add_field(name="Nitro", value=config.EMOJI_ISPREMIUM + interaction.user.premium_since if interaction.user.premium_since is not None else config.EMOJI_NOTPREMIUM + "Kein Nitro")
    return await interaction.followup.send(embed=embed)

class user_info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="benutzerinfo", description="Benutzer Informationen")
    async def benutzerinfo(self, interaction:discord.Interaction):
        await interaction.response.defer()
        await get_userinfo(interaction)
        return

    @app_commands.command(name="userinfo", description="Benutzer Informationen")
    async def userinfo(self, interaction:discord.Interaction):
        await interaction.response.defer()
        await get_userinfo(interaction)
        return
    
class userinfo_ctx(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.userinfo_ctx = app_commands.ContextMenu(
            name='Benutzer Info',
            callback=self.userinfo_ctx
        )
        self.client.tree.add_command(self.userinfo_ctx)

    async def cog_unload(self):
        self.client.tree.remove_command(self.userinfo_ctx.name, type=self.userinfo_ctx.type)

    async def userinfo_ctx(self, interaction: discord.Interaction, user: discord.User):
        await interaction.response.defer(ephemeral=True)
        await get_userinfo(interaction)
        return
        
async def setup(client):
    await client.add_cog(user_info(client))
    await client.add_cog(userinfo_ctx(client))
    print(__name__)
