import discord
from discord.ext import commands

import googleapiclient.discovery
from html import unescape
from json import loads
import re

def get_url(search_phrase: str):
    if not search_phrase.isprintable():
        return 'Invalid search phrase.'
    api_service_name = 'youtube'
    api_version = 'v3'
    key = ""
    try:
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=key)
    except googleapiclient.discovery.HttpError as e:
        content = loads(e.content)
        return content['error']['message']
    request = youtube.search().list(
        part='snippet',
        maxResults=25,
        order='relevance',
        q=search_phrase,
        type='video'
    )
    result = request.execute()
    if result.get('items'):
        video = result.get('items')[0]
        id = video.get('id').get('videoId')
        title = unescape(video.get('snippet').get('title'))
        return f'[ {title} ] - https://youtu.be/{id}'
    return 'No results.'

class Youtube(commands.Cog):
    """youtube search"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(usage="query", aliases=["youtube"])
    async def yt(self, ctx, *args):
        if match := re.match("\.(.*) (.*)", ctx.message.content):
            await ctx.send(get_url(match.groups()[1]))

def setup(bot):
    bot.add_cog(Youtube(bot))