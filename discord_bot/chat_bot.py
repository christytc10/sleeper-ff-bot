# Work with Python 3.6
from discord.ext import commands
from discord_bot.command_groups.trade_commands import TradeCommands
from discord_bot.command_groups.misc_commands import MiscCommands
import os


TOKEN = os.environ["CHAT_BOT_TOKEN"]
bot = commands.Bot(command_prefix='!')
bot.add_cog(TradeCommands(bot))
bot.add_cog(MiscCommands(bot))


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


def start_bot():
    bot.run(TOKEN)
