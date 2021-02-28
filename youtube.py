import discord
from discord.ext import commands

import googleapiclient.discovery
from html import unescape
from json import loads
import re

""" this explodes if you delete a post it is fucking with """

cool_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]

def get_videos(search_phrase: str):
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
        maxResults=5,
        order='relevance',
        q=search_phrase,
        type='video'
    )
    result = request.execute()
    if result.get('items'):
        return result.get('items')


class YouTubeSession(object):
    def __init__(self, user_id, links, message):
        self.user_id = user_id
        self.links = links
        self.message = message
        
class Youtube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.openQueries = {}

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id in self.openQueries:
            query = self.openQueries[payload.user_id]
            if query.message.id == payload.message_id:
                if payload.emoji.name in cool_emojis:
                    await query.message.edit(content=query.links[cool_emojis.index(payload.emoji.name)][1])
                    await query.message.clear_reactions()
                    del self.openQueries[payload.user_id]

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        if payload.cached_message.author.id in self.openQueries:
            del self.openQueries[payload.cached_message.author.id]

    @commands.command(usage="query", aliases=["youtube"])
    async def yt(self, ctx, *args):
        """searches youtube"""
        user = ctx.message.author
        if match := re.match("\.(yt|youtube) (.*)", ctx.message.content):
            query = match.groups()[1]
            if user.id in self.openQueries:
                # i feel like there is a lot wrong with what i am doing here.
                message = self.openQueries[user.id].message
                await message.edit(content=f"cancelled youtube query by {user.display_name}")
                await message.clear_reactions()
                del self.openQueries[user.id]
            if results := get_videos(query):
                links = []
                for video in results:
                    id = video.get('id').get('videoId')
                    title = unescape(video.get('snippet').get('title'))
                    links.append([title, f"https://youtu.be/{id}"])
                message = await ctx.reply(content="```"+"\n\n".join([result[0] for result in links]) + "```")
                for emoji, video in zip(cool_emojis, links):
                    await message.add_reaction(emoji)
                self.openQueries[user.id] = YouTubeSession(user.id, links, message)
            else:
                await ctx.send(content=f"```search for {query} yielded no results```")
        else:
            await ctx.send("invalid query, probably")

def setup(bot):
    bot.add_cog(Youtube(bot))