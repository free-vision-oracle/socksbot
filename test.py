import discord
from discord.ext import commands
        
class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message = None

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if not payload.user_id == self.bot.user.id:
            if payload.message_id == self.message.id:
                await self.message.edit(content="you hatched it!")
                await self.message.clear_reactions()
                await self.message.add_reaction("🐣")

    @commands.command()
    async def test(self, ctx, *args):
        """a simple test"""
        self.message = await ctx.reply("click on it")
        await self.message.add_reaction("🥚")

def setup(bot):
    bot.add_cog(Test(bot))