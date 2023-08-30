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
    
    @app_commands.command(name="autothreading", description="Bearbeite die Auto Thread Einstellungen")
    async def thread_overview(self, interaction: discord.Interaction):
        from cogs.settings.settingpage import goto_settinghome
        embed = await get_autothread_overview(interaction=interaction)
        await interaction.response.send_message(embed=embed, view=goto_settinghome())
        return
    
    @app_commands.command(name="autorename", description="Bearbeite die Auto Thread Rename Einstellungen")
    async def thread_overview(self, interaction: discord.Interaction):
        from cogs.settings.settingpage import goto_settinghome
        embed = await get_autothread_overview(interaction=interaction)
        await interaction.response.send_message(embed=embed, view=goto_settinghome())
        return
    
###
### AUTO THREAD RENAME SYSTEM
###
class autothread_threadrename(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        print(thread)
        name_module = "bread by GL" #append DB connection for name module
        await thread.edit(name=name_module)
        return
    
###
### AUTO THREADING SYSTEM
###
class autothread_threadrename(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        print(message)
        name_module = "bread by GL" #append DB connection for name module
        firstmsg_module = "First message container" #append DB connection for message module
        slowmode_module = 0 #append DB connection for message module
        char_min_limit = 10
        channels = []
        if len(message.content) >= char_min_limit:
            thread = await message.create_thread(name=name_module, reason="AutoThread", slowmode_delay=slowmode_module)
            await thread.send(firstmsg_module)
            #await create_thread(*, name, message=None, auto_archive_duration=..., type=None, reason=None, invitable=True, slowmode_delay=None)
            return
    
async def setup(client):
    await client.add_cog(autothread(client))
    await client.add_cog(autothread_threadrename(client))
    print(__name__)