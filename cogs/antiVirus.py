import apiTest
import custom
import discord
import validators
from discord.ext import commands

#https://validators.readthedocs.io/en/latest/#:~:text=%20Basic%20validators%20%C2%B6%20%201%20between%20%C2%B6.,Django%E2%80%99s%20email%20validator.%20Returns%20True%20on...%20More%20

numberOfEvil = 3

class antiVirus(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        buffer = message.content.split()
        for i in range(len(buffer)):
            if validators.url(buffer[i]):
                reports = apiTest.checkLink(buffer[i])
                if int(reports[1]) + int(reports[3]) >= numberOfEvil:
                    await message.guild.ban(message.author, reason=f"Mallicious: {reports[1]} Phishing: {reports[3]}")


def setup(client):
    client.add_cog(antiVirus(client))
