import discord
from discord.ext import commands, tasks
import re

card_pattern = "([0-9][SsCcDdHh])"

class Player(object):
    """player class for spades game"""
    def __init__(self, user):
        self.user = user
        self.hand = []
        self.bid = 0
        self.tricks = 0
        self.score = 0
        self.timeOut = 0

class Spades(commands.Cog):
    def __init__(self, bot):
        """the jailhouse classic"""
        self.bot = bot
        self.channel = None
        self.players = {}
        self.userIds = []
        self.turn = 0
        # 0: joining 1: bidding 2: playing
        self.stage = 0
        """ this can't be the way to do this... """
        for guild in self.bot.guilds:
            for channel in guild.channels:
                if channel.name == "cobb-county-adult-detention-center":
                    self.channel = channel
    
    def cog_check(self, ctx):
        if ctx.channel.name == "cobb-county-adult-detention-center":
            return True
        return False

    async def gameOver(self, ctx):
        self.stage = 0
        self.userIds = []
        players = sorted(self.players.values(), key=lambda player: player.score)
        scores = [f"{player.user.display_name}: {player.score}" for player in players]
        await ctx.send("scores:\n" + "\n".join(scores))
    
    @commands.guild_only()
    @commands.command()
    async def rules(self, ctx, *args):
        """displays game rules"""
        await ctx.send("the game is spades.\nthe rules can be found at:\nhttps://bicyclecards.com/how-to-play/spades/")

    @commands.guild_only()
    @commands.command()
    async def join(self, ctx, *args):
        """join a game of spades"""
        user = ctx.message.author
        if not user.id in self.players:
            self.players[user.id] = Player(user)
            if self.stage > 0:
                await ctx.reply("you'll be dealt in next hand")
                return
        await ctx.send("players:\n" + "\n".join(map(lambda player: player.user.display_name, self.players.values())))
    
    @commands.guild_only()
    @commands.command()
    async def start(self, ctx, *args):
        """start a game of spades"""
        if self.stage != 0:
            await ctx.send("is the game already started?")
            return
        if len(self.players) >= 2:
            await ctx.send("okay imma start the game!")
            self.userIds = list(map(lambda player: player.user.id, self.players.values()))
            self.turn = 0
            self.stage = 1
            await ctx.send(f"first to bid is {self.players[self.userIds[0]].user.mention}")
        else:
            await ctx.send("two players needed to start the game.")

    @commands.guild_only()
    @commands.command(usage="<number>")
    async def bid(self, ctx, *args):
        """bid how many tricks you think you'll win"""
        if self.stage != 1:
            await ctx.reply("it isn't time to bid")
            return
        if ctx.message.author.id == self.userIds[self.turn]:
            if match := re.match("\.bid ([0-9]+)", ctx.message.content):
                self.players[ctx.message.author.id].bid = int(match.groups()[0])
                self.turn += 1
                if self.turn == len(self.userIds):
                    self.turn = 0
                    await ctx.send("okay, all the bids are in.")
                    self.stage = 2
                else:
                    await ctx.send(f"got it. next is {self.players[self.userIds[self.turn]]}")
            else:
                await ctx.send("```.bid number```")
        else:
            await ctx.reply("it isn't your turn")    

    @commands.guild_only()
    @commands.command(aliases=["p"], usage="<number><suit> eg 4hearts or 4h")
    async def play(self, ctx, *args):
        """play a card"""
        if self.stage != 2:
            await ctx.send("nah. probably use .look")
            return
        if ctx.message.author.id == self.userIds[self.turn]:
            if match := re.matchAll("([0-9]{1:2}|[KkQqJjAa][SsCcHhDd])"):
                await ctx.reply("you tried to play " + "\n".join(match.groups()))
            else:
                await ctx.reply("one of us fucked up, lol")
        else:
            await ctx.reply("it isn't your turn")

    @commands.guild_only()
    @commands.command()
    async def quit(self, ctx, *args):
        """quit the game"""
        userId = ctx.message.author.user.id
        if userId in self.userIds:
            self.userIds.pop(self.userIds.index(userId))
        if userId in self.players:
            del self.players[userId]
            await ctx.send(f"{ctx.message.author.display_name} quit the game")
        if len(self.players) < 2:
            self.gameOver()

    @commands.guild_only()
    @commands.command()
    async def again(self, ctx, *args):
        """play again with the same players + whoever queued up"""
        pass

def setup(bot):
    bot.add_cog(Spades(bot))