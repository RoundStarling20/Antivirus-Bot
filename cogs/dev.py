import custom
import discord
from discord.ext import commands
from custom import directoryPath
from custom import emojiList

class dev(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_connect(self):
        print("Bot has connected to Discord!")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready!")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.command()
    @commands.check(custom.isItme)
    async def dump(self, ctx, dbName):
        await ctx.send(file=discord.File(f'cogs/Databases/{dbName}.json'))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def changePrefix(self, ctx, prefix):
        prefixes = custom.get_db(filePath=directoryPath["serverPrefixdb"])
        prefixes[str(ctx.guild.id)] = prefix
        custom.save_db(db=prefixes, filePath=directoryPath["serverPrefixdb"])
        await ctx.message.add_reaction(emojiList["confirmed"])

    @commands.command()
    @commands.check(custom.isItme)
    async def reload(self, ctx, extension):
        self.client.unload_extension(f'cogs.{extension}')
        self.client.load_extension(f'cogs.{extension}')
        await ctx.send(f'[{extension}] has been unloaded and reloaded')


def setup(client):
    client.add_cog(dev(client))