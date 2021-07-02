from Modules import Logger
from Cogs.RepostCog import Cog

import os
import discord
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

Log = Logger.Get("Main")
bot = commands.Bot("PI!")


@bot.event
async def on_ready():
    Log.info("Bot Ready")


bot.add_cog(Cog(bot))
bot.run(os.getenv("TOKEN"))