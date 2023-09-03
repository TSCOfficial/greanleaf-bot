import discord
from discord.ext import commands
from discord import ForumChannel, app_commands
import asyncio
from discord.utils import get

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
        #await interaction.response.defer()
        #await get_filter_overview(interaction)
        #return
        everyone = get(interaction.guild.roles, id=1128070513227485254)
        member = get(interaction.guild.roles, id=1128084058539307098)
        unverified = get(interaction.guild.roles, id=1147529039108640898)
        for channel in interaction.guild.channels:
            print(F"first layer: {channel}")
            if channel.type != discord.CategoryChannel:
                print(F"second layer: {channel}")
                if channel.permissions_for(everyone).view_channel != False or channel.permissions_for(member).view_channel != True or channel.permissions_for(member).read_message_history != True or channel.permissions_for(unverified).view_channel != False:
                    print(F"edit layer: {channel}")
                    print(channel)
                    perms = channel.overwrites_for(everyone)
                    perms.view_channel = False
                    await channel.set_permissions(everyone, overwrite=perms)

                    perms = channel.overwrites_for(member)
                    perms.read_message_history = True
                    perms.view_channel = True
                    await channel.set_permissions(member, overwrite=perms)

                    perms = channel.overwrites_for(unverified)
                    perms.view_channel = False
                    await channel.set_permissions(unverified, overwrite=perms)
                    await interaction.channel.send(f"{config.MSG_INLINE_CHECK} {channel.mention} Edit finished to 100% with set settings.")
                    await asyncio.sleep(305)
                else:
                    await interaction.channel.send(f"{config.MSG_INLINE_CHECK} {channel.mention} Edit finished with set settings.")
                    await asyncio.sleep(3)
        return

async def setup(bot):
    await bot.add_cog(filter(bot))
    print(__name__)