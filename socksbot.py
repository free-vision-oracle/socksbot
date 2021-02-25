import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import random
import re

description = '''love socks'''

intents = discord.Intents.default()
intents.reactions = True

deck = []
with open("cards.csv") as fh:
    deck = fh.read().split(",")

positions = ["thinking","feeling","doing"]

bot = commands.Bot(command_prefix='.', description=description, intents=intents)

extensions = ["basics", "spades", "youtube", "test"]
for e in extensions:
    bot.load_extension(e)

@bot.event
async def on_ready():
    print(f"my name is {bot.user.name} and i'm here to say, something that rhymes with my name!")

@bot.command()
@has_permissions(administrator=True)
async def reload(ctx, *args):
    """reload extensions"""
    if match := re.match("\.reload (.*)", ctx.message.content):
        match = match.groups()[0]
        if match in extensions:
            bot.reload_extension(match)
            print(f"{ctx.message.author.display_name} reloaded {match}")
            await ctx.reply("🐣")
            return
    await ctx.reply("🥚")

bot.run('')
