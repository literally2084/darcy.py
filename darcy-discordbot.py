# darcy.py, a simple discord.py bot, by novaur!

# imports

import requests
import discord
import aiohttp
import random
import time
import re
import os

from discord.ext import commands # important for setting up commands
from discord.ext.commands import has_permissions # allows for requiring specific perms for preforming specific cmds or actions


print("[discordpy.darcella.bot]: installing discord pkgs . . .") # log, informs that required packages will be installed
try:
    os.system('pip3 install -q discord.py py-cord') # try to install discord.py and pycord packages
    print("[installed discord pkgs successfully!]") # success
except Exception as e: # except if error/exception
    print(e) # print exception

intents = discord.Intents.all() # define intents

# define the bot client,
# enable intents (intents enables the bot to oversee specific events),
# and disable the bot from pinging @everyone or roles!
bot = discord.Bot(intents=intents, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False))

# no help command needed, slash commands are used
bot.help_command = None

# the token. the equivalent to the password/key of a bot: BE SURE TO HIDE THIS SOMEWHERE SAFE.
TOKEN = ("[INSERT_TOKEN_HERE]") # you would enter your token here

@bot.event # event: run...
async def on_ready(): # ...when ready to be hosted
    # ^^^^ also, discord.py is built on top of the Python asyncio framework to prevent issues with the bot freezing when handling tasks
    print(f"We have logged in as {bot.user}") # darcella is logged into discord!
    try:
        synced = await bot.sync_commands()
        print(f"[discordpy.darcella.bot]: synced slash command(s)!") # attempt to sync commands
    except Exception as e:
        print(e) # if that fails, print error(s) ("e" used to store the error/exception object)
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(type=discord.ActivityType.playing, name="with you!") # set discord status to "Playing with you!"
    )

@bot.event # event: run on...
async def on_member_join(member): # ...every person that joins the bot's discord server,
    channel = bot.get_channel(1483829497144016957) #get channel by channel ID
    await channel.send(f"{member} has joined the server!") # send welcome message regarding new users in channel!

# leave response list of strings
leaveResponse = ["decided to leave.", "has left the server.", "backed out and left the server."] 

@bot.event
async def on_member_remove(member): # on every person the leaves the bot's discord server,
    channel = bot.get_channel(1483829497144016957) # get channel by channel ID
    await channel.send(f"{member} " + random.choice(leaveResponse)) # grab from the leave responses list a random string and send it!
    
userPings = {} # store user and a number in dictionary that gets updated to represent the # of times they pinged the bot
@bot.event
async def on_message(message): # on every message event
    if message.author.id not in userPings: # if user not within the userPings dictionary
        userPings[message.author.id] = (0) # add the user into the list with a starting value of 0
    userPings[message.author.id] += 1 # add 1 to their value, this value represents number of times the user has pinged the bot!
    userPingsValue = userPings[message.author.id]
    # greet: list of greeting strings
    greet = ["Yo!", "Hiya!", "Sup?", "Hi.", "Hello :)", "Howdy!", f"Hello there, {message.author.name}!\n\n Fun fact: you have pinged me **{userPingsValue}** times in total!"]
    if bot.user in message.mentions: # if anyone messages the bot pinging them, 
      await message.channel.send(random.choice(greet), reference=message) # make the bot reply to pinging messages with a random message in the greet list variable
    # await bot.process_commands(message) # ensure commands are still processing correctly

# ctx (aka commands.Context, required to be the first parameter in every bot command), acts as a container for storing background info regarding cmds.
# example: if a user uses a bot's command, ctx allows the bot to recall that user via "ctx.author" or other information
@bot.command(description="Purge/mass delete messages! (manage_messages are required)")
async def clear(ctx, amount: int = 2):
  if ctx.author.guild_permissions.manage_messages: # if the user calling cmd has manage messages perms,
      await ctx.channel.purge(limit=amount) # purge [amount (2 is default)] messages in channel
      await ctx.respond("Done! :)", ephemeral=True) # send message only to author (aka user who ran the slash cmd)
  else:
      await ctx.send("Invalid permissions.") # otherwise, notify the user doesn't have permission to use cmd

@bot.command(description="Make me say anything!")
async def speak(ctx, *, message: str = None): # message --> multi-word string parameter, optional
    if message == None:
        await ctx.respond(f"{ctx.author}, don't forget to enter a message for me to say! X(", ephemeral=True) # if no message is entered by a user, notify user
    else:
        await ctx.send(message) # send set message

bot.run(TOKEN) # run using token