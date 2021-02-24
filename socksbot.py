import discord
from discord.ext import commands
import random
import re

description = '''love socks'''

intents = discord.Intents.default()

deck = []
with open("cards.csv") as fh:
    deck = fh.read().split(",")

positions = ["thinking","feeling","doing"]

bot = commands.Bot(command_prefix='.', description=description, intents=intents)

extensions = ["basics", "spades", "youtube"]
for e in extensions:
    bot.load_extension(e)

@bot.event
async def on_ready():
    print(f"my name is {bot.user.name} and i'm here to say, something that rhymes with my name!")

@bot.command()
async def reload(ctx, *args):
    """reload extensions"""
    if ctx.author.top_role.name == "egg layers" or ctx.author.top_role.name == "The Socks":
        if match := re.match("\.reload (.*)", ctx.message.content):
            if match.groups()[0] in extensions:
                bot.reload_extension(match.groups()[0])
                await ctx.reply("🐣")
                return
    await ctx.reply("🥚")

bot.run('')
