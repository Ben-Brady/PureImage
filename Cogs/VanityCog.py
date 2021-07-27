from Modules import Logger, Guilds

import random
import discord
from discord.ext import commands, tasks

Log = Logger.Get("VanityCog")

Statuses = [
    [discord.Streaming, "over your memes channels"],
    [discord.Game, "with your users"]
]


class Cog(commands.Cog):
    """A cog for handling vanity functions such as Status changes"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        Log.info("Initialised")

    @tasks.loop(seconds=2)
    async def ChangeStatus(self):
        Selection = random.randint(0, len(Statuses) - 1)
        Activity, Message = Statuses[Selection]
        await bot.change_presence(game=discord.Game(name="Test", type=1))
        # await self.bot.change_presence(activity=Activity(name=Message))
        Log.debug(f"Changed presence to status {Selection}")

    @commands.guild_only()
    async def UpdateSettings(self, ctx: commands.Context):
        Guild = Guilds.Get(ctx.guild.id)
