import apiVT
import custom
import discord
import validators
from discord.ext import commands
from custom import directoryPath

#https://validators.readthedocs.io/en/latest/#:~:text=%20Basic%20validators%20%C2%B6%20%201%20between%20%C2%B6.,Django%E2%80%99s%20email%20validator.%20Returns%20True%20on...%20More%20

numberOfEvil = 3

class antiVirus(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        db = custom.get_db(filePath=directoryPath["urlDB"])
        buffer = message.content.split()
        inVerified = 0
        inChecked = 0
        for i in range(len(buffer)):
            if validators.url(buffer[i]):
                #Check each dictionary for similar link
                for x in range(len(db["verified"])):
                    if db["verified"][x] in buffer[i]:
                        inVerified = 1
                for x in range(len(db["checkedURLS"])):
                    if db["checkedURLS"][x] in buffer[i]:
                        inChecked = 1
                if  not(inVerified or inChecked):
                    reports = await apiVT.checkLink(buffer[i])
                    if reports["malicious"] >= numberOfEvil:
                        await message.author.edit(roles=[])
                        role = discord.utils.get(message.guild.roles, name="Muted")
                        await message.author.add_roles(role, reason= "Mallicious: " + str(reports["malicious"]))
                        await message.delete()
                        return
                    else:
                        db["checkedURLS"].append(buffer[i])
                        custom.save_db(db, filePath=directoryPath["urlDB"])


def setup(client):
    client.add_cog(antiVirus(client))