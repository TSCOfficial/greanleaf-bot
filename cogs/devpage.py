import discord
from discord.ext import commands

class devpage(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot



async def setup(bot):
    await bot.add_cog(devpage(bot))
    print(__name__)