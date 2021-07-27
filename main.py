from Modules import Logger
from Cogs import RepostCog, SettingsCog, VanityCog

import os
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

Log = Logger.Get("root")
bot = commands.Bot("~")

Log.info("New Session Started")

@bot.event
async def on_ready():
    Log.info("Bot Ready")

bot.add_cog(RepostCog.Cog(bot))
bot.add_cog(SettingsCog.Cog(bot))
# bot.add_cog(VanityCog.Cog(bot))
# bot.add_cog(PornCog.Cog(bot))

bot.run(os.getenv("TOKEN"))