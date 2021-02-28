import discord
from discord.ext import commands, tasks
import re
import time

card_pattern = "([0-9][SsCcDdHh])"

wait_time = 10.0


class Game(object):
    """state for spades games"""
    def __init__(self, channel):
        pass

class Player(object):
    """player class for spades game"""
    def __init__(self, user, teammate, channel_id):
        pass

class Spades(commands.Cog):
    def __init__(self, bot):
        """the jailhouse classic"""
        spass

    def cog_check(self, ctx):
        # needs to do a real check, lol
        return False

    @commands.guild_only()
    @commands.command(usage="@teammate")
    async def join(self, ctx, *args):
        """joins a game of spades"""
        pass

def setup(bot):
    bot.add_cog(Spades(bot))