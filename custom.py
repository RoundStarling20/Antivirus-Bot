import datetime as dt
import json
import os
from collections import OrderedDict

import discord
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from discord.ext import commands

import apiVT

directoryPath = {
  "serverPrefixdb": "cogs/Databases/prefixes.json",
  "urlDB": "cogs/Databases/listOfURLS.json",
  "apiUse":"/home/pi/Documents/AVBot/Images/apiCalls.png"
}

emojiList = {
    "confirmed": "<a:confirmed:881422225134223372>",
    "failed": "<a:failed:881422274467598366>"
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

async def getDaily():
    x = {}
    data = await apiVT.getUseage()

    for value in data['data']['daily']:
                if 'url' in str(data['data']['daily'][value]):
                    x[value] = data['data']['daily'][value]['/api/v3/(url_submission)'] + data['data']['daily'][f'{value}']['/api/v3/(urls)']

    x = OrderedDict(sorted(x.items(), key=lambda t: t[0]))
    
    return x

async def graphDates():
    os.remove(directoryPath["apiUse"])
    dates = []
    apiUses = []
    data = await getDaily()
    for values in data:
        dates.append(values)
        apiUses.append(data[values])
    dates = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]
    
    #Begin Formatting plot
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.plot(dates,apiUses,'#00a3b6')
    plt.gcf().autofmt_xdate()
    plt.ylabel('Number of API Calls')
    plt.xlabel('Date')
    plt.grid(True)
    plt.savefig(directoryPath["apiUse"])