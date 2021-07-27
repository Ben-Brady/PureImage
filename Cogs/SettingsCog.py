from io import StringIO
from Modules import Logger, PornDetector, Guilds

from pathlib import Path
import requests
import discord
from discord.ext import commands

Log = Logger.Get("SettingsCog")
DocStore = Path("./Data/Documentation.zip")
SettingsLink = r"https://github.com/ThatGayKid/PureImage"


class Cog(commands.Cog):
    """A Cog for checking new messages for Porn"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        Log.info("Initialised")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        if not Guilds.Check(guild.id):
            await guild.owner.send("""> Read the repo in order to get setup:
                                   https://github.com/thatgaykid/pureimage""")

    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.command(name="id")
    async def GetID(self, ctx: commands.Context):
        await ctx.reply(ctx.channel.id)
        
    
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.command(name="set")
    async def UpdateSettings(self, ctx: commands.Context):
        Guild = Guilds.Get(ctx.guild.id)
        Attachments = ctx.message.attachments
        if not Attachments:
            Settings = StringIO(Guild.SettingJSON)
            await ctx.reply("> Need to include a file, Current Settings:",
                    file=discord.File(Settings,filename='Settings.json'))
        else:
            Settings = await Attachments[0].read()
            try:
                Guild.LoadJSON(Settings.decode())
            except AssertionError:
                await ctx.reply("> Invalid Settings Values")
            except Guilds.json.JSONDecodeError:
                await ctx.reply("> Error Parsing JSON")
            else:
                await ctx.reply("> Settings Changed Successfully")
