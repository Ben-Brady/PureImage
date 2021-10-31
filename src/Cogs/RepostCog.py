from Modules import Logger, Reposts, Guilds
from typing import List, Tuple
from discord.ext import commands
import discord
from datetime import datetime


Log = Logger.Get("RepostCog")


class Cog(commands.Cog):
    """A Cog for checking new messages to if they're reposts"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        Log.info("Initialised")

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        Guild = Guilds.Get(msg.guild.id)

        if not Guild.rEnabled:
            return
        if msg.channel.id not in Guild.rChannels:
            return

        async for Type,Attachment in self.AssessAttachments(msg.attachments):
            OriginID = 0
            File = await Attachment.read()

            if Type == "image":
                exists, OriginID = Reposts.CheckImage(msg.guild.id, File)
            elif Type == "video":
                exists, OriginID = Reposts.CheckVideo(msg.guild.id, File)
            else:
                Log.debug(f"File from {msg.id} ignored due to invalid filetype ({Type})")

            # If the message is new, then add it
            if not exists:
                await self.Add(msg, Attachment)
                return 
            
            # If original message is deleted, remove it from the list and return
            try:
                Log.debug(f"Fetching message with id {OriginID}")
                OriginMSG = await msg.channel.fetch_message(OriginID)
            except discord.errors.NotFound:
                Log.debug(f"Error find message with id {OriginID}")
                Reposts.Remove(OriginID)
                await self.Add(msg, Attachment)
                return
            else:
                Log.debug(f"Success finding message with id {OriginID}")

            # If the message is older than the threshold, remove it from the list and return
            TimeDelta = OriginMSG.created_at - datetime.now()
            if TimeDelta.total_seconds() > Guild.rTimeout:
                Reposts.Remove(msg.id)
                await self.Add(msg, Attachment)
            else:
                # Otherwise, call out the original message as a repost
                BotMSG = await OriginMSG.reply(
                    Guild.msgRepostDetected.format(
                        AUTHOR=msg.author.mention,
                        author=msg.author.name,
                        ORIGIN=OriginMSG.author.mention,
                        origin=OriginMSG.author.name
                    )
                )
                await BotMSG.delete(delay=10)

                if Guild.rDelete:
                    await msg.delete(delay=10)
        
    async def Add(self, msg: discord.Message, Attachment: discord.Attachment):
        File = await Attachment.read()
        Type = Attachment.content_type.split("/")[0]

        if Type == "image":
            Reposts.AddImage(msg.id, msg.guild.id, File)
        elif Type == "video":
            Reposts.AddVideo(msg.id, msg.guild.id, File)

    async def AssessAttachments(self,Attachments:List[discord.Attachment]) -> Tuple[str,discord.Attachment]:
        for Attachment in Attachments:
            Type = Attachment.content_type.split("/")[0]
            if Attachment.size > 4_000_000:
                Log.debug(f"File ignored due to size of {Attachment.size} bytes")
                continue
            
            if Type == "image":
                Size = (Attachment.height * Attachment.width)
                if Size < 10_000_000:
                    yield "image",Attachment
            elif Type == "video":
                yield "video",Attachment
            else:
                Log.debug(f"Filetype {Type} ignored due to unsupported, {Type}")