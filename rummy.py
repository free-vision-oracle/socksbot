import discord
from discord.ext import commands

suits = ["♠","♣","♦","♥"]
ranks = [n for n in range(2,10)] + ["ace", "jack", "queen", "king"]

class Player(object):
    def __init__(self, user):
        self.user = user
        self.hand = []
        self.score = 0

class Rummy(commands.Cog):
    """jailhouse rummy"""
    def __init__(self, bot):
        self.bot = bot
        self.stock = []
        self.discard = []
        self.players = []
        self.turn = -1
        self.queue = []

    async def cog_check(self, ctx):


    @commands.guild_only()
    @commands.command(usage="")
    async def join(self, ctx, *args):
        """join a game of rummy"""
        if self.turn < 0 and not ctx.message.author in self.players:
            self.players.append(Player(ctx.message.author))
            message = "players:\n" + "\n".join(map(lambda player: player.user.display_name, self.players))
            await ctx.send(message)
        elif userId in self.players:
            await ctx.send("you've already joined")
        else:
            await ctx.send("you'll be joined at the end of this round")
    @commands.guild_only()
    @commands.command(usage="deck|discard")
    async def draw(self, ctx, *args):
        """draw a card"""
        pass
    @commands.guild_only()
    @commands.command(usage="")
    async def flip(self, ctx, *args):
        """discard -> stock"""
        pass
    @commands.guild_only()
    @commands.command(aliases=["meld", "layoff"])
    async def play(usage="<number><suit>"):
        """put cards on the table"""
        pass
    @commands.guild_only()
    @commands.command(usage="")
    async def discard(self, ctx, *args):
        """discard a card and end your turn"""
        pass
    @commands.guild_only()
    @commands.command(usage="")
    async def quit(self, ctx, *args):
        """leave the game"""
        userId = ctx.message.author.id
        if userId in self.players:
            del self.players[ctx.message.author.id]
        elif userId in self.queue:
            self.queue.pop(self.queue.index(userId))
        else:
            await ctx.reply("were you playing?")
            return
        await ctx.reply("you quit the game (and lost)")
    @commands.guild_only()
    @commands.command(usage="")
    async def rules(self, ctx, *args):
        """displays a summary of the game's rules"""
        await ctx.send("basically like this:\nhttps://bicyclecards.com/how-to-play/rummy-rum/\nonly jailhouse style.")
    @commands.guild_only()
    @commands.command()
    async def start(self, ctx, *args):
        """starts a game of rummy"""
        await ctx.send("🚨🚧under🚧construction🚧🚨")
    
    async def roundOver(self, ctx):
        """fired at the conclusion of a round"""
        pass

    async def gameOver(self, ctx):
        """fired when someone's score >= 500"""
        pass

def setup(bot):
    bot.add_cog(Rummy(bot))
                
            