import custom
import discord
from discord.ext import commands


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

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 882472664860594327:
            print("AntiVirusBot responded")
        else:
            print(f"{message.author} said {message.content}")

    @commands.command()
    @commands.check(custom.isItme)
    async def reload(self, ctx, extension):
        self.client.unload_extension(f'cogs.{extension}')
        self.client.load_extension(f'cogs.{extension}')
        await ctx.send(f'[{extension}] has been unloaded and reloaded')


def setup(client):
    client.add_cog(dev(client))
