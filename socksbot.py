# This example requires the 'members' privileged intents

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

mention_pattern = ".* "

bot = commands.Bot(command_prefix='.', description=description, intents=intents)

def getCards(count: int):
    cards = [n for n in deck]
    random.shuffle(cards)
    result = []
    for _ in range(count):
        result.append(cards.pop())
    return result

@bot.event
async def on_ready():
    print(f"my name is {bot.user.name}#{bot.user.id} and i'm here to say")
    print("something that rhymes with my name")

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command()
async def choose(ctx, *args):
    """Chooses between multiple choices."""
    choices = re.match("\.choose (.*)", ctx.message.content).groups()[0]
    choices = choices.split(" OR ")
    if len(choices):
        await ctx.send(random.choice(choices))

@bot.command()
async def shouldi(ctx, *args):
    await ctx.reply(random.choice(["yes", "maybe", "no"]))

@bot.command()
async def freevision(ctx, *args):
    """Stripped down version of the Free Vision Oracle"""
    if query := re.match("\.freevision (.*)", ctx.message.content):
        query = query.groups()[0]
        reply = f"```diff\n-{query}\n" + "\n".join([f"-•{position}: {card}" for position, card in zip(positions, getCards(3))]) + "```"
        await ctx.reply(reply)
    else:
        await ctx.send("https://free-vision-oracle.neocities.org\n```.freevision <query>```")

@bot.command()
async def role(ctx, *args):
    result = ""
    for user in ctx.message.mentions:
        result = result + f"{user.name}'s top role is: {user.top_role.name}"
    if not result:
        result = f"{ctx.message.author.name}'s top role is {ctx.message.author.top_role.name}"
    await ctx.send(result)

bot.run('')
