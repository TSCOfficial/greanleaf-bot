from email import message
import discord
from discord.ext import commands
from discord.utils import get
from discord.app_commands import AppCommandError, CommandNotFound, MissingPermissions, Choice
from discord import app_commands
import mysql.connector

import config as config
from config import conf

async def get_autothread_overview(interaction: discord.Interaction, channel:int=None):
    embed = await conf().EMBED(
        interaction=interaction,
        title="Auto Thread",
        description="Bearbeite die Auto Thread EInstellungen des Servers.",
    )
    embed.add_field(name="Auto Thread", value="Thread Einstellungen ändern.\ncmd", inline=False)

    connection = await conf().DB_con()
    cursor = connection.cursor()
    if channel is not None:
        cursor.execute(f"SELECT guild, thread_channel, thread_name, thread_message, thread_minchars, thread_cooldown, thread_exceptbot FROM thread WHERE thread_channel = {channel}")
    else:
        cursor.execute(f"SELECT guild, thread_channel, thread_name, thread_message, thread_minchars, thread_cooldown, thread_exceptbot FROM thread WHERE guild = {interaction.guild.id}")
    result = cursor.fetchall()# -> [(guild, channel, ..)] 
    if result != list():
        for thread in result:
            print(thread)
            embed.add_field(name="Thread setting", value=thread, inline=False)

    
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
        channel="Kanal eingeben inwelchem Auto Threading aktiviert sein soll*",
        name="Thread Name eingeben (Siehe Thread Übersicht für variabeln)*",
        nachricht="Erste Thread Nachricht eingeben",
        charachter="Mindest Charachter Limit für Threadestellung eingeben",
        cooldown="Schreibcooldown in Sekunden eingeben",
        bots="Erlaube das Threading für Bot Nachrichten"
        )
    @app_commands.choices(
        bots=[
            Choice(name="Ja, Bots einbinden", value=1),
            Choice(name="Nein, Bots ausschliessen", value=0)
        ]
    )
    async def thread_autothread(self, interaction: discord.Interaction,
                                channel:discord.TextChannel=None,
                                name:str=None,
                                nachricht:str=None,
                                charachter:int=None,
                                cooldown:int=None,
                                bots:int=0
                                ):
        from cogs.settings.settingpage import goto_settinghome
        embed = await get_autothread_overview(interaction=interaction)
        connection = await conf().DB_con()
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM thread WHERE guild = {interaction.guild.id}")
        result = cursor.fetchall()# -> [(guild, channel)]
        print(result)      
        if name is None and nachricht is None and charachter is None and cooldown is None and channel is None:
            await interaction.response.send_message(embed=embed, view=goto_settinghome())
            return
        
        elif name is None or channel is None:
            await interaction.response.send_message(
                content="Einpaar Eingaben für das fehlerfreie ausführen des Autothreadings fehler.", 
                embed=embed,
                view=goto_settinghome())
            return
        
    
        else:
            if len(result) >= config.LIMIT_AUTOTHREAD:
                await interaction.response.send_message(
                content=f"Das Autothread Limit ({config.LIMIT_AUTOTHREAD}) wurde erreicht!", 
                embed=embed,
                view=goto_settinghome())
                return
            cursor.execute(f"SELECT guild, thread_channel FROM thread WHERE guild = {interaction.guild.id} AND thread_channel = {channel.id}")
            result = cursor.fetchall()# -> [(guild, channel)] 
            print(result)  
            if result == list():
                sql = "INSERT INTO thread (guild, thread_channel, thread_name, thread_message, thread_minchars, thread_cooldown, thread_exceptbot) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val = (interaction.guild.id, channel.id, name, nachricht, charachter, cooldown, bots)
                cursor.execute(sql, val)
                connection.commit()
                await interaction.response.send_message(content="inserted")
                return
            
            elif interaction.guild.id == result[0][0] and channel.id == result[0][1]:
                charachter = "NULL" if charachter is None else charachter
                cooldown = "NULL" if cooldown is None else cooldown
                cursor.execute(f"UPDATE thread SET `thread_name`='{name}', `thread_message`='{nachricht}', `thread_minchars`={charachter}, `thread_cooldown`={cooldown}, `thread_exceptbot`={bots} WHERE `guild`={interaction.guild.id} AND `thread_channel`={channel.id}")
                connection.commit()
                await interaction.response.send_message(content="updated")
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
        print(message.content)
        connection = await conf().DB_con()
        cursor = connection.cursor()
        cursor.execute(f"SELECT guild, thread_name, thread_message, thread_minchars, thread_cooldown, thread_channel, thread_exceptbot FROM thread")
        result = list(cursor.fetchall())
        i = 0
        for thread in result:
            name_module = result[i][1]
            firstmsg_module = result[i][2]
            char_min_limit = int(result[i][3]) if result[i][3] else 0
            slowmode_module = int(result[i][4]) if result[i][4] else 0
            channel = result[i][5]
            bots = result[i][6] #1 = True, 0 = False

            if message.channel.id == channel and len(message.content) > char_min_limit:
                if not message.author.bot or (message.author.bot and bots == 1): #user is not bot, or user is bot and bot allowed
                    thread = await message.create_thread(name=name_module, reason="AutoThread", slowmode_delay=slowmode_module)
                    if firstmsg_module is not None:
                        await thread.send(firstmsg_module)
            i += 1
            
        
async def setup(client):
    await client.add_cog(autothread(client))
    await client.add_cog(autothread_threadrename(client))
    print(__name__)