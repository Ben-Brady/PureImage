
from discord.ext import commands
import discord
from Modules import Logger, Reposts, Guilds

from datetime import datetime

Log = Logger.Get("RepostCog")


class Cog(commands.Cog):
    """A Cog for checking new messages to if they're reposts"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.RecentDeleted = []
        Log.info("Initialised")

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        Guild = Guilds.Get(msg.guild.id)

        if not Guild.rEnabled:
            return
        if msg.channel.id not in Guild.rChannels:
            return
        for Attach in msg.attachments:
            await self.Process(msg, Attach)

    @commands.Cog.listener()
    async def on_message_delete(self, msg: discord.Message):
        if msg.author == self.bot:
            return
        if msg.id in self.RecentDeleted:
            self.RecentDeleted.remove(msg.id)
            return

        Log.debug(f"Removed post '{msg.id}'")
        Reposts.Remove(msg.id)

    async def Process(self, msg: discord.Message, Attachment: discord.Attachment):
        Guild = Guilds.Get(msg.guild.id)
        Type = Attachment.content_type.split("/")[0]
        OriginID = 0
        if Attachment.size > 8_000_000:
            Log.debug(
                f"File from {msg.id} ignored due to size of {Attachment.size} bytes")
            return

        File = await Attachment.read()

        if Type == "image":
            Size = (Attachment.height * Attachment.width)
            if Size > 10_000_000:
                Log.debug(
                    f"Image from {msg.id} ignored due pixel count of {Size} from {msg.author}")
            else:
                OriginID = Reposts.CheckImage(msg.guild.id, File)
        elif Type == "video":
            OriginID = Reposts.CheckVideo(msg.guild.id, File)
        else:
            Log.debug(f"File from {msg.id} ignored due to invalid file")

        # ToDo: Refactor this messy code
        if OriginID:
            try:
                OriginMSG = await msg.channel.fetch_message(OriginID)
            except discord.errors.NotFound:
                Reposts.Remove(msg.id)
            else:
                Delta = discord.Message.created_at - datetime.now()

                if Delta < Guild.rTimeout:
                    BotMSG = await OriginMSG.reply(
                        Guild.GetMsg("rDetect").format(
                            AUTHOR=msg.author.mention,
                            author=msg.author.name,
                            ORIGIN=OriginMSG.author.mention,
                            origin=OriginMSG.author.name
                        )
                    )
                    await BotMSG.delete(delay=10)

                    if Guild.rDelete:
                        self.RecentDeleted.append(msg.id)
                        await msg.delete(delay=5)
                else:
                    Reposts.Remove(msg.id)
                    await self.Add(msg, Attachment)
        else:
            await self.Add(msg, Attachment)

    async def Add(self, msg: discord.Message, Attachment: discord.Attachment):
        Type = Attachment.content_type.split("/")[0]
        File = await Attachment.read()

        if Type == "image":
            Reposts.AddImage(msg.id, msg.guild.id, File)
        elif Type == "video":
            Reposts.AddVideo(msg.id, msg.guild.id, File)
