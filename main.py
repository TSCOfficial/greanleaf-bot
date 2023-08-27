import discord
from discord.ext import commands, tasks
import pytz
from datetime import datetime
import asyncio
from typing import Literal, Optional
from discord.ext.commands import Greedy
import json
import os

#config
import config as config
from config import conf, error_rapport_del

timezone = pytz.timezone("Europe/Berlin")

format = "%H:%M:%S"
now_EU = datetime.now(pytz.timezone('UTC')).astimezone(pytz.timezone('Europe/Zurich'))

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="g.",
            intents=discord.Intents.all(),
            application_id=config.CLIENT_APPLICATION_ID
            )

    async def on_ready(self):
        print(f'BotId: {client.user.id} - Name: {client.user.name} - Status: {config.CLIENT_STATUS} - Zeit: {now_EU.strftime(format)} Ping: {round(client.latency *1000)}')
        me = client.get_user(618876411905835018)
        await client.change_presence(status=config.CLIENT_STATUS, activity=discord.Game(f'By {me.display_name}'))
        try:
            cursor = await conf().DB_con()
            print(f"[{now_EU.strftime(format)}] ✅ | Verbindung zur Datenbank wurde hergestellt.")
        except:
            print(f"[{now_EU.strftime(format)}] ❌ | Verbindung zur Datenbank konnte nicht hergestellt werden!\nDas System wird heruntergefahren.")
            return exit(404)
        while True:
            cursor = await conf().DB_con()
            if cursor is None:
                print(f"[{now_EU.strftime(format)}] ❌ | Verbindung zur Datenbank konnte nicht hergestellt werden!\nDas System wird heruntergefahren.")
                return exit(404)
            await asyncio.sleep(300) #5min
            
            
        
    async def setup_hook(self):
        """Import Buttons for Forceload"""
        self.add_view(error_rapport_del())
    
        await self.load_extension(f"config")

        await self.load_extension(f"cogs.devpage")
        await self.load_extension(f"cogs.settingpage")

        await self.load_extension(f"cogs.info_only.bot_info")
        await self.load_extension(f"cogs.info_only.user_info")

client = MyBot()

@client.command()
@commands.guild_only()
async def sync(ctx, guilds: Greedy[discord.Object], spec: Optional[Literal["gl"]] = None) -> None:
    if ctx.author.id == config.USER_ME_ID:
        try:
            if not guilds:
                if spec == "gl":
                    synced = await ctx.bot.tree.sync()
                else:
                    synced = await ctx.bot.tree.sync(guild=ctx.guild)

                return await ctx.send(
                    f"**Syncronisierung - {'Global' if spec is not None else 'Server'}**\n"
                    f"{len(synced)} application_commands wurden mit dem `@app_command.{'global' if spec is not None else 'local'}-tree` Syncronisiert."
                )
        except Exception as e:
            return await ctx.send(f"**Syncronisierung Fehlgeschlagen!**\nRatelimit exceeded. Bitte versuche es in einpaar Minuten erneut.```{e}```")
    return await ctx.reply(conf().EMBED_ERROR_PERMISSION(description="ctx.author.id == config.USER_ME_ID"))
        
client.run('MTE0MzUxOTIxNDQ5MDEwMzgzMg.GMEV01.6Iz1qNoJZIGTFRMnMADtpn7bdccxBX8rsxUeSw')