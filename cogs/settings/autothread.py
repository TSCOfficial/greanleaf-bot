import discord
from discord.ext import commands
from discord.utils import get
from discord.app_commands import AppCommandError, CommandNotFound, MissingPermissions, Choice
from discord import app_commands
import mysql.connector

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

    @app_commands.command(
            name="übersicht",
            description="Übersicht der aktuellen Einstellungen",
            )
    async def thread_overview(self, interaction: discord.Interaction):
        from cogs.settings.settingpage import goto_settinghome
        embed = await get_autothread_overview(interaction=interaction)
        await interaction.response.send_message(embed=embed, view=goto_settinghome())
        return
    
    @app_commands.command(
            name="autothreading",
            description="Bearbeite die Auto Thread Einstellungen",
            )
    @app_commands.describe(
        name="Thread Name eingeben (Siehe Thread Übersicht für variabeln)",
        nachricht="Erste Thread Nachricht eingeben",
        charachter="Mindest Charachter Limit für Threadestellung eingeben",
        cooldown="Schreibcooldown in Sekunden eingeben",
        channel="Kanal eingeben inwelchem Auto Threading aktiviert sein soll.",
        )
    async def thread_autothread(self, interaction: discord.Interaction,
                              name:str=None,
                              nachricht:str=None,
                              charachter:int=None,
                              cooldown:int=None,
                              channel:discord.TextChannel=None):
        from cogs.settings.settingpage import goto_settinghome
        embed = await get_autothread_overview(interaction=interaction)
        connection = await conf().DB_con()
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM thread WHERE guild = {interaction.guild.id}")
        result = cursor.fetchall()
        print(result)
        print(type(result))        
        if name is None and nachricht is None and charachter is None and cooldown is None and channel is None:
            await interaction.response.send_message(embed=embed, view=goto_settinghome())
            return
        
        elif name is None or channel is None:
            await interaction.response.send_message(
                content="Einpaar Eingaben für das fehlerfreie ausführen des Autothreadings fehler.", 
                embed=embed,
                view=goto_settinghome())
            return
        
        elif result == list():
            sql = "INSERT INTO thread (guild, thread_channel, thread_name, thread_minchars, thread_cooldown) VALUES (%s, %s, %s, %s, %s)"
            val = (interaction.guild.id, channel.id, name, charachter, cooldown)
            cursor.execute(sql, val)
            connection.commit()
            await interaction.response.send_message(content="inserted")
            return
        
        else:
            print("Error thread_autothread")
            return
    
    @app_commands.command(
            name="autorename",
            description="Bearbeite die Auto Thread Rename Einstellungen",
            )
    async def thread_autorename(self, interaction: discord.Interaction):
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
    async def on_message(self, message: discord.Message):
        print(message)
        connection = await conf().DB_con()
        cursor = connection.cursor()
        cursor.execute(f"SELECT guild, thread_name, thread_message, thread_minchars, thread_cooldown, thread_channel FROM thread")
        result = list(cursor.fetchone())

        name_module = result[1]
        firstmsg_module = result[2]
        char_min_limit = int(result[3]) if result[3] else None
        slowmode_module = int(result[4]) if result[4] else None
        channel = result[5]

        if message.channel.id == channel and len(message.content) > char_min_limit:      
            thread = await message.create_thread(name=name_module, reason="AutoThread", slowmode_delay=slowmode_module)
            await thread.send(firstmsg_module)
            return
    
async def setup(client):
    await client.add_cog(autothread(client))
    await client.add_cog(autothread_threadrename(client))
    print(__name__)