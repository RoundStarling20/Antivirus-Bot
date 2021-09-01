import json

import discord
from discord.ext import commands

directoryPath = {
  "serverPrefixdb": "cogs\Databases\prefixes.json"
}


def isItme(ctx):
    return ctx.message.author.id == 220327217312432129

def isItKing(author):
    king = {220327217312432129, 870467770846945290}
    return (author in king)

def get_db(filePath):
    with open(filePath, "r") as file:
        return json.load(file)

def save_db(db, filePath):
    with open(filePath, "w") as file:
        json.dump(db, file, indent=4)

def getPrefix(client, message):
    prefixes = get_db(filePath=directoryPath["serverPrefixdb"])
    return prefixes[str(message.guild.id)]

def addTwo(input):
    return input + 2