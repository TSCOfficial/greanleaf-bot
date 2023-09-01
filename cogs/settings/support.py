from typing import Optional
import discord
from discord.ext import commands
from discord import app_commands

import config as config
from config import conf

async def get_support_overview(interaction: discord.Interaction):
    embed = await conf().EMBED(
        interaction=interaction,
        title="Support",
        description="Bearbeite die Support Einstellungen des Servers.",
    )
    return embed

async def get_support_ticket_settings(interaction: discord.Interaction):
    embed = await conf().EMBED(
        interaction=interaction,
        title="Ticket Support",
        description="Bearbeite die Ticket Support Einstellungen des Servers.",
    )
    return embed

async def get_support_talk_settings(interaction: discord.Interaction):
    embed = await conf().EMBED(
        interaction=interaction,
        title="Support Talk",
        description="Bearbeite die Support Talk Einstellungen des Servers.",
    )
    return embed

class support_buttons(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="Ticket", custom_id="support_ticket_settings")
    async def support_ticket(self, interaction: discord.Interaction, button: discord.Button):
        from cogs.settings.settingpage import goto_settinghome
        embed = await get_support_ticket_settings(interaction=interaction)
        await interaction.response.edit_message(embed=embed, view=goto_settinghome())
        return
    
    @discord.ui.button(style=discord.ButtonStyle.blurple, label="Talk", custom_id="support_talk_settings")
    async def support_talk(self, interaction: discord.Interaction, button: discord.Button):
        from cogs.settings.settingpage import goto_settinghome
        embed = await get_support_talk_settings(interaction=interaction)
        await interaction.response.edit_message(embed=embed, view=goto_settinghome())
        return

class support_system(commands.GroupCog, name="support"):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(name="übersicht", description="Übersicht der aktuellen Einstellungen")
    async def support_overview(self, interaction: discord.Interaction):
        embed = await get_support_overview(interaction=interaction)
        await interaction.response.send_message(embed=embed, view=support_buttons())
        return

    @app_commands.command(name="ticket", description="Ticket Support Einstellungen bearbeiten")
    async def support_ticket(self, interaction: discord.Interaction):
        from cogs.settings.settingpage import goto_settinghome
        embed = await get_support_ticket_settings(interaction=interaction)
        await interaction.response.send_message(embed=embed, view=goto_settinghome())
        return
    
    @app_commands.command(name="talk", description="Support Talk Einstellungen bearbeiten")
    async def support_talk(self, interaction: discord.Interaction):
        from cogs.settings.settingpage import goto_settinghome
        embed = await get_support_talk_settings(interaction=interaction)
        await interaction.response.send_message(embed=embed, view=goto_settinghome())
        return

async def setup(bot):
    await bot.add_cog(support_system(bot))
    print(__name__)