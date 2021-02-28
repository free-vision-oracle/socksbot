import discord
from discord.ext import commands
import re

class Admin(commands.Cog):
    """adminitrative tools"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not 804776267470995456 in map(lambda role: role.id, member.roles):
            await member.add_roles(discord.Object(804776267470995456))
    
    @commands.has_permissions(administrator=True)
    @commands.command(usage="@mention")
    async def roles(self, ctx):
        """display a user's roles"""
        user = ctx.message.mentions[0]
        message = f"```\nroles report for {user.display_name}\n"
        message = message + "\n".join([f"{role.name}: {role.id}" for role in user.roles])
        message = message + "```"
        await ctx.send(message)
        
    @commands.has_permissions(administrator=True)
    @commands.command(usage="message")
    async def message(self, ctx):
        """a bad idea"""
        if match := re.match("\.message (.*)", ctx.message.content):
            for channel in self.bot.get_all_channels():
                if channel.name == "love-socks":
                    await channel.send(match.groups()[0])
        
def setup(bot):
    bot.add_cog(Admin(bot))
