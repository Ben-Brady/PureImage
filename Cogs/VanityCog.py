from Modules import Logger, Guilds

import random
import discord
from discord.ext import commands, tasks

Log = Logger.Get("VanityCog")


class Cog(commands.Cog):
    """A cog for handling vanity functions such as Status changes"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        Log.info("Initialised")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        "Announcement that a guild has invited the bot"
        owner = self.bot.fetch_user(self.bot.owner_id)
        owner.send(f"Yay, {guild.name} is the {len(self.bot.guilds)}th server.")
    
    # @tasks.loop(seconds=5)
    # async def ChangeStatus(self):
    #     Selection = random.randint(0, len(Statuses) - 1)
    #     Activity, Message = Statuses[Selection]
    #     # await self.bot.change_presence(activity=Activity(name=Message))
    #     Log.debug(f"Changed presence to status {Selection}")