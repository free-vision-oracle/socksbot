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

@bot.event
async def on_message(message):
    if not message.author == bot.user:
        if name := re.match(".*[Ss]ocks.*", message.author.display_name):
            if re.match("love me", message.content):
                await message.reply("love socks")
    await bot.process_commands(message)

@bot.command()
async def roll(ctx, dice: str):
    """rolls a dice"""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('```.roll <int>n<int>```')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command(usage="this OR that")
async def choose(ctx, *args):
    """chooses between multiple choices"""
    if not args:
        await ctx.send("```.choose this OR that```")
        return
    choices = re.match("\.choose (.*)", ctx.message.content).groups()[0]
    choices = choices.split(" OR ")
    if len(choices):
        await ctx.send(random.choice(choices))

@bot.command(usage="do a thing")
async def shouldi(ctx, *args):
    """ask yes or no questions"""
    await ctx.reply(random.choice(["yes", "maybe", "no"]))

@bot.command(usage="query")
async def freevision(ctx, *args):
    """free vision oracle"""
    if query := re.match("\.freevision (.*)", ctx.message.content):
        query = query.groups()[0]
        reply = f"```diff\n-{query}\n" + "\n".join([f"-•{position}: {card}" for position, card in zip(positions, getCards(3))]) + "```"
        await ctx.reply(reply)
    else:
        await ctx.send("https://free-vision-oracle.neocities.org\n```.freevision <query>```")

@bot.command(usage="@mention")
async def role(ctx, *args):
    """displays a user's top role"""
    result = ""
    for user in ctx.message.mentions:
        result = result + f"{user.name}'s top role is: {user.top_role.name}"
    if not result:
        result = f"{ctx.message.author.name}'s top role is {ctx.message.author.top_role.name}"
    await ctx.send(result)

@bot.command(usage="noun", aliases=["smoking"])
async def smokin(ctx):
    """indicates you're smoking something"""
    verb = random.choice(["blazing", "atomizing", "re-imagining", "really considering", "fully integrating"])
    adjective = random.choice(["seriously impressive", "actually insane", "actual", "of that good good", "for real", "mother fucking"])
    if match := re.match("\.smokin (.*)", ctx.message.content):
        await ctx.send(f"{ctx.message.author.display_name} is {verb} some {adjective} {match.groups()[0]}")
    else:
        noun = random.choice(["business", "secret shit", "goodness", "brain realignment"])
        await ctx.send(f"{ctx.message.author.display_name} is {verb} some {adjective} {noun}")

bot.run('')
