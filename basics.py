import discord
from discord.ext import commands
import random
import itertools
import re


class Basics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.deck = []
        # this is stupid as fuck
        with open("cards.csv") as fh:
            self.deck = fh.read().split(",")
        self.positions = ["thinking","feeling","doing"]

    def getCards(self, count: int):
        cards = [n for n in self.deck]
        random.shuffle(cards)
        result = []
        for _ in range(count):
            result.append(cards.pop())
        return result

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author == self.bot.user:
            if name := re.match(".*[Ss]ocks.*", message.author.display_name):
                if re.match("love me\?", message.content):
                    await message.reply("yes, love socks")
                elif re.match("love me\.?", message.content):
                    await message.reply("love socks")

    @commands.command(usage="<number>")
    async def d(self, ctx, *args):
        """rolls a dice"""
        if match := re.match(".d (-?[0-9]*)", ctx.message.content):
            try:
                value = int(match.groups()[0])
                await ctx.send(f"d{value}: {random.randint(min([0,value]), max([0,value]))}")
            except TypeError:
                pass
            except Exception:
                pass
        else:
            await ctx.send("```.d <number>```")

    @commands.command(usage="this OR that")
    async def choose(self, ctx, *args):
        """chooses between multiple choices"""
        if not args:
            await ctx.send("```.choose this OR that```")
            return
        choices = re.match("\.choose (.*)", ctx.message.content).groups()[0]
        choices = choices.split(" OR ")
        if len(choices):
            await ctx.send(random.choice(choices))

    @commands.command(usage="do a thing")
    async def shouldi(self, ctx, *args):
        """ask yes or no questions"""
        await ctx.reply(random.choice(["yes", "maybe", "no"]))

    @commands.command(usage="query")
    async def freevision(self, ctx, *args):
        """free vision oracle"""
        if query := re.match("\.freevision (.*)", ctx.message.content):
            query = query.groups()[0]
            reply = f"```diff\n-{query}\n" + "\n".join([f"-•{position}: {card}" for position, card in zip(self.positions, self.getCards(3))]) + "```"
            await ctx.reply(reply)
        else:
            await ctx.send("https://free-vision-oracle.neocities.org\n```.freevision <query>```")

    @commands.command(usage="@mention")
    async def role(self, ctx, *args):
        """displays a user's top role"""
        result = ""
        for user in ctx.message.mentions:
            result = result + f"{user.name}'s top role is: {user.top_role.name}"
        if not result:
            result = f"{ctx.message.author.name}'s top role is {ctx.message.author.top_role.name}"
        await ctx.send(result)

    @commands.command(usage="<noun>", aliases=["smoking"])
    async def smokin(self, ctx):
        """indicates you're smoking something"""
        verb = random.choice(["blazing", "atomizing", "re-imagining", "really considering", "fully integrating"])
        adjective = random.choice(["seriously impressive", "actually insane", "actual", "of that good good", "for real", "mother fucking"])
        if match := re.match("\.smokin (.*)", ctx.message.content):
            await ctx.send(f"{ctx.message.author.display_name} is {verb} some {adjective} {match.groups()[0]}")
        else:
            noun = random.choice(["chronic","good shit", "business", "secret shit", "goodness", "brain realignment"])
            await ctx.send(f"{ctx.message.author.display_name} is {verb} some {adjective} {noun}")

def setup(bot):
    bot.add_cog(Basics(bot))