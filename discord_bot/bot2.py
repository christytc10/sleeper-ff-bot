from discord.ext import commands
import os

TOKEN = os.environ["CHAT_BOT_TOKEN"]
bot = commands.Bot(command_prefix='!')


@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run(TOKEN)
