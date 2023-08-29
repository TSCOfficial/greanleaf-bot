import discord
from discord.ext import commands
from discord.utils import get
from discord.app_commands import AppCommandError, CommandNotFound, MissingPermissions, Choice
from discord import Interaction, app_commands

import config as config
from config import conf
from cogs.settings.autothread import get_autothread_overview

async def get_settings_overview(interaction):
    embed = await conf().EMBED(
        interaction=interaction,
        title="Einstellungen",
        description="Sämtliche Server und Bot Einstellungen ansehen und bearbeiten.",
    )
    embed.add_field(name="Auto Thread", value="Thread Einstellungen ändern.\ncmd", inline=False)
    embed.add_field(name="Loggin", value="Log Einstellungen ändern.\ncmd", inline=False)
    embed.add_field(name="URL/Link Filter", value="Filter Einstellungen ändern.\ncmd", inline=False)
    embed.add_field(name="Support System", value="Support Einstellungen ändern.\n"
                    "- Ticket System\n"
                    "- Support Talk Benachrichtigung\n", inline=False)
    return embed


### SETTINGS OVERVIEW
class settings(commands.GroupCog, name="einstellung"):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(name="übersicht", description="Übersicht der aktuellen einstellungen")
    async def setting_overview(self, interaction: discord.Interaction):
        embed = await get_settings_overview(interaction=interaction)
        await interaction.response.send_message(embed=embed, view=setting_buttons())
        return
    
class setting_buttons(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(style=discord.ButtonStyle.gray, label="Auto Thread", custom_id="setting_autothread", emoji=config.EMOJI_THREAD)
    async def goto_autothread(self, interaction: discord.Interaction, button: discord.Button):
        embed = await get_autothread_overview(interaction=interaction)
        await interaction.response.edit_message(embed=embed, view=goto_settinghome())
        return
    
    @discord.ui.button(style=discord.ButtonStyle.gray, label="Support System", custom_id="setting_supsystem", emoji=config.EMOJI_TICKET)
    async def goto_supsystem(self, interaction: discord.Interaction, button: discord.Button):
        embed = await get_autothread_overview(interaction=interaction)
        await interaction.response.edit_message(embed=embed, view=goto_settinghome())
        return
    
    @discord.ui.button(style=discord.ButtonStyle.gray, label="URL Filter", custom_id="setting_filter", emoji=config.EMOJI_FILTER)
    async def goto_urlfilter(self, interaction: discord.Interaction, button: discord.Button):
        embed = await get_autothread_overview(interaction=interaction)
        await interaction.response.edit_message(embed=embed, view=goto_settinghome())
        return
    
    @discord.ui.button(style=discord.ButtonStyle.gray, label="Logs", custom_id="setting_logs", emoji=config.EMOJI_LOGS)
    async def goto_logs(self, interaction: discord.Interaction, button: discord.Button):
        embed = await get_autothread_overview(interaction=interaction)
        await interaction.response.edit_message(embed=embed, view=goto_settinghome())
        return

class goto_settinghome(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="Home", custom_id="setting_home")
    async def setting_home(self, interaction: discord.Interaction, button: discord.Button):
        embed = await get_settings_overview(interaction=interaction)
        await interaction.response.edit_message(embed=embed, view=setting_buttons())
        return

async def setup(client):
    await client.add_cog(settings(client))
    print(__name__)