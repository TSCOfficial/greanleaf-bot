import discord
from discord.ext import commands
from discord.utils import get
import mysql.connector
import inspect
from typing import Literal, Optional
from discord.ext.commands import Greedy
from typing import TypedDict

class load_config(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

#### RELATIVE VARIABLES
"""FOR DATABASE CONNECTION AND CURSOR CALLING"""

#### FIXED VARIABLES
### COLORS - ! change colors !
COLOR_EMBED = 0x2b2d31 #no embed color
COLOR_RED = COLOR_ERROR = 0xe74c3c #flatUI
COLOR_ORANGE = 0xe67e22 #flatUI
COLOR_YELLOW = 0xf1c40f #flatUI
COLOR_GREEN = 0x2ecc71 #flatUI

### ICONS/EMOJIS (standard icon color: #babbbf, in svg main: viewBox="-2 -2 +2 +2", in path: stroke="#babbbf" stroke-width="0.5" fill="current-color", size: 128)
EMOJI_BOX_DISABLED = None
EMOJI_BOX_ENABLED = None
EMOJI_BOX_UNSET = "<:unset:1144659729105289347>"
EMOJI_TOGGLE_DISABLED = None
EMOJI_TOGGLE_ENABLED = None
EMOJI_ISPREMIUM = "<:is_premium:1144538490072203284>"
EMOJI_NOTPREMIUM = "<:not_premium:1144529568435273798>"
EMOJI_HASH = "<:hash:1144663717527699517>"

### USERS
USER_ME_ID = 618876411905835018
USER_ME_MENTION = f"<@{USER_ME_ID}>"
## CLIENT
CLIENT_STATUS = discord.Status.idle
CLIENT_APPLICATION_ID = 1143519214490103832

### GUILDS
GUILD_SUPPORTSERVER_ID = 000000
## CATEGORIES
# CHANNELS
CHANNEL_SUPPORTSERVER_ERRORLOG = 000000

### MESSAGE TEMPLATES
## MSG Component
MSG_INLINE_CHECK = "✅ **|**"


class conf(): #wait conf().
    async def DB_con(self):
        db = mysql.connector.connect(
            host= "webhost-05.hosmatic.com",
            user= "s6435_Arlo",
            password= "Server.Streaky007",
            database= "s6435_test")
        return db.cursor()
    
    async def EMBED_ERROR_PERMISSION(self, description:str=None): #add missing permissions in data when callback -> ex.:"user.permission returned False"
        meta = await conf().files(description)
        title = "Fehlende Berechtigungen"
        text = "Du bist nicht berechtigt, diese Interaktion auszuführen."
        embed = discord.Embed(description=f"### {title}\n{text}\n```{meta}```", color=COLOR_RED)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1088501912585912401/1088501967346728960/7qnJwbX.png")
        embed.set_footer(text="Für mehr Informationen, wende dich an die Serverleitung.")
        return embed
    
    async def EMBED_ERROR_SLASH(self, description:str=None): #add error in data when callback (error variable)
        meta = await conf().files(description)
        title = "Slashbefehl fehlgeschlagen"
        text = "Ein fehler ist aufgetreten. Ein Raport wurde bereits den Entwicklern weitergeleitet."
        embed = discord.Embed(description=f"### {title}\n{text}\n```{meta}```", color=COLOR_RED)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1088501912585912401/1088501967346728960/7qnJwbX.png")
        embed.set_footer(text="Für mehr Informationen, wende dich an die Serverleitung.")
        return embed
    
    async def EMBED_ERROR_GLOBAL(self, description:str=None, fieldname:str=None):
        title = "Interaktion fehlgeschlagen"
        if len(fieldname) == 1:
            embed = discord.Embed(description=f"### {title}\n{description}", color=COLOR_RED)
        else:
            embed = discord.Embed(description=f"### {title}", color=COLOR_RED)
            embed.add_field(name=fieldname, value=description)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1088501912585912401/1088501967346728960/7qnJwbX.png")
        embed.set_footer(text="Für mehr Informationen, wende dich an die Serverleitung.")
        return embed
    
    async def EMBED_RAPPORT(self, interaction=None):
        meta = await conf().files(interaction)
        title = "Fehler Rapport"
        text = "Ein unerwarteter Fehler ist aufgetreten."
        embed = discord.Embed(description=f"### {title}\n{text}\n```{meta}```", color=COLOR_RED)
        embed.set_footer(text="Developer error handeler")
        guild = interaction.client.get_guild(GUILD_SUPPORTSERVER_ID)
        sys_notify = get(guild.channels, id=CHANNEL_SUPPORTSERVER_ERRORLOG)
        return await sys_notify.send(embed=embed, view=error_rapport_del())
    
    async def files(self, *data):
        frame = inspect.currentframe().f_back.f_back
        func = frame.f_code.co_name
        file = inspect.getframeinfo(frame).filename
        line = inspect.getframeinfo(frame).lineno
        code_ctx = inspect.getframeinfo(frame).code_context
        if file.startswith("c:"):
            file = "filename N/A"
        return f"{str(code_ctx[0]).strip()}\nOn Line {line}\n{file}: async def {func}(*):\n{data[1]}" if data[1] else f"{file}: async def {func}(*):"
    

    async def EMBED(self, interaction=None,
                    title:str=None,
                    description:str=None,
                    color:Optional[int]=COLOR_EMBED,
                    image:str=None,
                    footer:str=None,
                    footer_url:str=None,
                    thumbnail_url:str=None,
                    request:bool=None
                    ):
        footer_icon = interaction.client.get_user(USER_ME_ID).display_avatar if footer_url is None else footer_url
        embed = discord.Embed(title=title, description=description, color=color)
        embed.set_image(url=image)
        embed.set_thumbnail(url=thumbnail_url)
        if request is True and footer_url is None and footer is None:
            embed.set_footer(icon_url=interaction.user.display_avatar, text=f"Abfrage von {interaction.user.name}")
        else:
            embed.set_footer(icon_url=footer_icon, text="GreanLeaf Bot by Aliz" if footer is None else footer)
        return embed
    
class error_rapport_del(discord.ui.View):
    def __init__(self, *data) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(style=discord.ButtonStyle.green, label="Erledigt", custom_id="delete_errorrapport")
    async def error_rapport_delete(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user.id == USER_ME_ID:
            await interaction.message.delete()
            await interaction.response.send_message(f"{MSG_INLINE_CHECK} Rapport wurde als __Erledigt__ Markiert.", ephemeral=True)
            return
        else:
            return await interaction.response.send_message(embed=await conf().EMBED_ERROR_PERMISSION("interaction.user.id == USER_ME_ID returned False"), ephemeral=True)


async def setup(bot):
    await bot.add_cog(load_config(bot))
    print(__name__)