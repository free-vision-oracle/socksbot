import discord
from discord.ext import commands, tasks
import re
import time

card_pattern = "([0-9][SsCcDdHh])"

wait_time = 10.0

class Player(object):
    """player class for spades game"""
    def __init__(self, user, teammate, channel_id):
        self.user = user
        self.hand = []
        self.bid = 0
        self.tricks = 0
        self.score = 0
        self.waiting_since = time.time()
        self.teammate = teammate
        self.channel_id # this is just because i don't know what i'm doing probably

    def tick(self):
        if time.time() > self.waiting_since + wait_time:
            return False
        return True

class Spades(commands.Cog):
    def __init__(self, bot):
        """the jailhouse classic"""
        self.bot = bot
        self.players = {}
    
    def cog_check(self, ctx):
        if ctx.channel.name == "cobb-county-adult-detention-center" or ctx.channel.name == "really-though":
            return True
        return False

    @commands.guild_only()
    @commands.command(usage="@teammate")
    async def join(self, ctx, *args):
        """joins a game of spades"""
        await ctx.send("```not implemented```")
        return
        mentions = ctx.message.mentions
        if mentions:
            if not len(mentions) == 1:
                await ctx.reply("you need to mention your teammate")
                return
            else:
                target = mentions[0]
                if target.id in self.players:
                    if self.players[target.id].teammate.id == ctx.message.author.id:
                        await ctx.reply(f"your teammate is: {self.players[target.id].user.display_name}")
                        # this is where we confirm a dyad by removing the timer thingy and adding the second person
                    else:
                        await ctx.reply("looks like they already have a teammate")
                        return
                else:
                    player = Player(ctx.message.author, target)
                    self.players[ctx.message.author.id] = player
                    self.waiting.append(player)


def setup(bot):
    bot.add_cog(Spades(bot))