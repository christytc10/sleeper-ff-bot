# Work with Python 3.6
import discord
from player_value import find_value
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


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
