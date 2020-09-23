# Work with Python 3.6
import discord
from discord_bot.player_value import find_value, similar_value
from discord_bot.combine import get_combine_results
import os

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


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


def start_bot():
    client.run(TOKEN)
