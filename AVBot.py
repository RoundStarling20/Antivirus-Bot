import os

import discord
from discord import file
from discord.ext import commands
from discord.flags import Intents

import custom
from custom import directoryPath

client = commands.Bot(command_prefix = custom.getPrefix)

@client.event
async def on_guild_join(guild):
    prefixes = custom.get_db(filePath=directoryPath["serverPrefixdb"])
    prefixes[str(guild.id)] = '.'
    custom.save_db(db=prefixes, filePath=directoryPath["serverPrefixdb"])

@client.event
async def on_guild_remove(guild):
    prefixes = custom.get_db(filePath=directoryPath["serverPrefixdb"])
    prefixes.pop(str(guild.id))
    custom.save_db(db=prefixes, filePath=directoryPath["serverPrefixdb"])

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.CommandNotFound):
            await ctx.send("This is not a command.")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f'cogs.{filename[:-3]}')


with open("token.txt", 'r', encoding="utf-8") as fp:
    client.run(f"{fp.read()}")