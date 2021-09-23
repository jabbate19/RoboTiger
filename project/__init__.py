""""
Copyright © Krypton 2021 - https://github.com/kkrypt0nn
Description:
This is a template to create your own discord bot in python.
https://www.reddit.com/r/FTC/new/.json?count=20
Version: 3.0
"""

import json
import os
import platform
import sys
import math
import time
import requests as r
import discord
from discord.ext import tasks
from discord.ext.commands import Bot

"""	
Setup bot intents (events restrictions)
For more information about intents, please go to the following websites:
https://discordpy.readthedocs.io/en/latest/intents.html
https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents


Default Intents:
intents.messages = True
intents.reactions = True
intents.guilds = True
intents.emojis = True
intents.bans = True
intents.guild_typing = False
intents.typing = False
intents.dm_messages = False
intents.dm_reactions = False
intents.dm_typing = False
intents.guild_messages = True
intents.guild_reactions = True
intents.integrations = True
intents.invites = True
intents.voice_states = False
intents.webhooks = False

Privileged Intents (Needs to be enabled on dev page), please use them only if you need them:
intents.presences = True
intents.members = True
"""

intents = discord.Intents.default()

bot = Bot(command_prefix='them good memes', intents=intents)
#client = discord.Client()
last_time_checked=time.time()

# The code in this even is executed when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    last_time_checked=time.time()
    status_task.start()


# Setup the game status task of the bot
@tasks.loop(minutes=5.0)
async def status_task():
    global last_time_checked
    await bot.change_presence(activity=discord.Game("them good memes"))
    posts = r.get('https://www.reddit.com/r/FTC/new/.json', headers = {'User-agent': 'your bot 0.1'})
    posts = posts.json()
    posts = posts['data']['children']
    memes = [ x for x in posts if ( x['data']['link_flair_text'] == 'Meme' and x['data']['created_utc'] > last_time_checked ) ]
    memes.reverse()
    for meme in memes:
        embed=discord.Embed(title="New Meme on r/FTC", description="Behold, Meme!", color=0xe67e22, url="https://reddit.com" + meme['data']['permalink'])
        embed.set_author(name=meme['data']['author'], url='https://reddit.com/u/'+meme['data']['author'])
        embed.add_field(name=meme['data']['title'], value=":arrow_down: :arrow_down: :arrow_down:", inline=False)
        url = meme['data']['url']
        if url[-4:] == ".jpg" or url[-4:] == ".png" or url[-5:] == ".jpeg":
            embed.set_image(url=meme['data']['url'])
        channel = bot.get_channel(890416261396324382)
        await channel.send(embed=embed)
    last_time_checked = math.floor(time.time())


# Removes the default help command of discord.py to be able to create our custom help command.
bot.remove_command("help")
'''
if __name__ == "__main__":
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")
'''

# The code in this event is executed every time someone sends a message, with or without the prefix
@bot.event
async def on_message(message):
    # Ignores if a command is being executed by a bot or by the bot itself
    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)

# The code in this event is executed every time a valid commands catches an error
@bot.event
async def on_command_error(context, error):
    raise error


# Run the bot with the token
bot.run(os.environ.get('DISCORD'))
