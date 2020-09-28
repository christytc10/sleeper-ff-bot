# Work with Python 3.6
import discord
from discord_bot.player_value import find_value, similar_value
from discord_bot.combine import get_combine_results
from discord_bot.snaps import get_snap_counts
from discord_bot.weekly_stats import get_weekly_stats
import os
import re

TOKEN = os.environ["CHAT_BOT_TOKEN"]
client = discord.Client()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

    if message.content.startswith('!value'):
        name = message.content[len('!value'):].strip()
        await message.channel.send(find_value(name))

    if message.content.startswith('!similar'):
        name = message.content[len('!similar'):].strip()
        await message.channel.send(similar_value(name))

    if message.content.startswith('!combine'):
        name = message.content[len('!combine'):].strip()
        await message.channel.send(get_combine_results(name))

    if message.content.startswith('!snaps'):
        name = message.content[len('!snaps'):].strip()
        await message.channel.send(get_snap_counts(name))

    if message.content.startswith('!week'):
        week = re.findall('\d+', message.content)[0]
        print(week)
        print(message.content[message.content.find(week) + len(week):].strip())
        name = message.content[message.content.find(week) + len(week):].strip()
        await message.channel.send(get_weekly_stats(name, week))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


def start_bot():
    client.run(TOKEN)
