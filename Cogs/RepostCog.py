from Modules import Logger, Reposts
from Modules.Guild import Guilds

from discord.ext import commands
import discord
import re


class Cog(commands.Cog):
    """A Cog for checking new messages"""

    def __init__(self, bot: commands.Bot):
        self.Log = Logger.Get("Reposts")
        self.bot = bot

        self.Log.info("RepostCog Initialised")
        self.RecentDeleted = []

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        GuildID = str(msg.guild.id)
        Guild = Guilds[GuildID]
        Section = Guild.Section

        for Attach in msg.attachments:
            if not re.search("^image/", Attach.content_type):
                continue
            if (Attach.height * Attach.width) > 10_000_000:
                continue

            img = await Attach.read()
            RepostID = Section.Check(img)

            if RepostID:

                try:
                    RepostMessage = await msg.channel.fetch_message(RepostID)
                except discord.errors.NotFound:
                    Section.Remove(msg.id)
                else:
                    self.Log.debug(
                        f"Repost between '{RepostID}' and '{msg.id}'")
                    BotMSG = await RepostMessage.reply(f"{msg.author.mention}, Uh oh a repost!")

                    await BotMSG.delete(delay=10)
                    if Guild.DeletePost:
                        self.RecentDeleted.append(msg.id)
                        await msg.delete(delay=5)
                    return

            Section.Add(msg.id, img)

    @commands.Cog.listener()
    async def on_message_delete(self, msg: discord.Message):
        if msg.author == self.bot:
            return
        if msg.id in self.RecentDeleted:
            self.RecentDeleted.remove(msg.id)
            return

        self.Log.debug(f"Removed post '{msg.id}'")
        guild = Guilds[msg.guild.id]
        guild.Section.Remove(msg.id)
