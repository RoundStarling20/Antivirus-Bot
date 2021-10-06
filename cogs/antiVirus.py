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
        #doesnt delete bot messages
        if not(message.author.bot):
            db = custom.get_db(filePath=directoryPath["urlDB"])
            badDB = custom.get_db(filePath=directoryPath["badURLDB"])
            buffer = message.content.split()
            inVerified = False
            inChecked = False
            for i in range(len(buffer)):
                if validators.url(buffer[i]):

                    #checks to see if link is in databse of malicious urls
                    for x in range(len(badDB["malicious"])):
                        if badDB["malicious"][x] in buffer[i]:
                            try:
                                #get user roles, check for muted role
                                role = discord.utils.get(message.guild.roles, name="Muted")
                                if role not in message.author.roles:
                                    channel = message.guild.get_channel(854918297505759283)
                                    await channel.send(f"{message.author.mention} has sent a link previously marked as mallicious and has been muted")

                                    #remove roles, add muted
                                    await message.author.edit(roles=[])
                                    role = discord.utils.get(message.guild.roles, name="Muted")
                                    await message.author.add_roles(role, reason= "Sent a link in the malicious database ")
                            except:
                                print("Link in database error")
                            finally:
                                await message.delete()
                                print("This link is in the malicious database")
                            return


                    print(buffer[i])
                    #Check each dictionary for similar link
                    #Cant return because the entire message needs to be checked for multiple links
                    for x in range(len(db["verified"])):
                        if db["verified"][x] in buffer[i]:
                            inVerified = True
                            print("In Verified")
                    if not inVerified:
                        for x in range(len(db["checkedURLS"])):
                            if db["checkedURLS"][x] in buffer[i]:
                                inChecked = True
                                print("In Checked")


                    if  not(inVerified or inChecked):
                        reports = await apiVT.checkLink(buffer[i])
                        if reports["malicious"] >= numberOfEvil:
                            try:
                                #checks to see if user has been muted
                                role = discord.utils.get(message.guild.roles, name="Muted")
                                if role not in message.author.roles:
                                    channel = message.guild.get_channel(854918297505759283)
                                    await channel.send(f"{message.author.mention} has sent a malicious link with {str(reports['malicious'])} flags and they have been muted.")

                                    #removes roles, adds muted
                                    await message.author.edit(roles=[])
                                    role = discord.utils.get(message.guild.roles, name="Muted")
                                    await message.author.add_roles(role, reason= "Mallicious: " + str(reports["malicious"]))

                            except:
                                print("The user was either kicked or left the server")
                                
                            finally:
                                badDB["malicious"].append(buffer[i])
                                custom.save_db(badDB, filePath=directoryPath["badURLDB"])
                                await message.delete()
                            return
                        
                        else:
                            db["checkedURLS"].append(buffer[i])
                            custom.save_db(db, filePath=directoryPath["urlDB"])
                            print("Added to the Checked URL's")


    @commands.command()
    @commands.check(custom.isItme)
    async def apiUse(self, ctx):
        await custom.graphDates()
        await ctx.send(file=discord.File(directoryPath["apiUse"]))


def setup(client):
    client.add_cog(antiVirus(client))