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

bot.load_extension("basics")

@bot.event
async def on_ready():
    print(f"my name is {bot.user.name} and i'm here to say, something that rhymes with my name!")

bot.run('')
