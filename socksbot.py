#!/usr/local/bin/python
import discord
import re

client = discord.Client()

@client.event
async def on_ready():
    print(f"My name is {client.user} and i'm here to say, something that rhymes, with my name")


@client.event
async def on_message(m):
    if m.author == client.user:
        return
    msg = m.content.lower().split(" ")
    if client.user in m.mentions:
      await m.channel.send("🥚")
      return

client.run('ODEyODcyMTk3OTM2OTA2MjYy.YDHEOg.UEekRKVJRe4Aknq2ohuhqCFNV4s')