from Modules import Logger, PornDetector, Guilds

from discord.ext import commands
import discord
import re

Log = Logger.Get("PornCog")


class Cog(commands.Cog):
    """A Cog for checking new messages for Porn"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        Log.info("Initialised")

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        Guild = Guilds.Get(msg.guild.id)

        if not Guild.pEnabled:
            return

        for Attach in msg.attachments:
            await self.process(msg, Attach)

    async def process(self, msg: discord.Message, Attach: discord.Attachment):
        Guild = Guilds.Get(msg.guild.id)

        if not Attach.content_type.split("/")[0] == "image":
            return
        elif (Attach.height * Attach.width) > 10_000_000:
            return

        img = await Attach.read()
        Certainty = PornDetector.Check(img)
        if Certainty > Guild.pThreshold:
            BotMSG = await msg.reply(
                Guild.GetMsg("pDelete").format(
                    AUTHOR=msg.author.mention,
                    author=msg.author.name,
                    certainty=Certainty
                )
            )
            await BotMSG.delete(delay=10)
            await msg.delete()
