# Work with Python 3.6
from discord.ext import commands
from discord_bot.player_value import find_value, similar_value
from discord_bot.combine import get_combine_results
from discord_bot.snaps import get_snap_counts
from discord_bot.weekly_stats import get_weekly_stats, get_player_stat
from discord_bot.card_check import get_injured_starters
from discord_bot.roster_analysis import get_roster_ages, get_roster_value
import os

TOKEN = os.environ["CHAT_BOT_TOKEN"]
bot = commands.Bot(command_prefix='!')


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def value(ctx, player_name):
    await ctx.send(find_value(player_name))


@bot.command()
async def combine(ctx, player_name):
    await ctx.send(get_combine_results(player_name))


@bot.command()
async def cardcheck(ctx):
    await ctx.send(get_injured_starters())


@bot.command()
async def stat(ctx, name, stat_name):
    await ctx.send(get_player_stat(name, stat_name))


@bot.command()
async def snaps(ctx, player_name):
    await ctx.send(get_snap_counts(player_name))


@bot.command()
async def roster_ages(ctx):
    await ctx.send(get_roster_ages())


@bot.command()
async def roster_value(ctx):
    await ctx.send(get_roster_value())


@bot.command()
async def similar(ctx, player_name):
    await ctx.send(similar_value(player_name))


@bot.command()
async def week(ctx, nfl_week, player_name):
    await ctx.send(get_weekly_stats(player_name, nfl_week))


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


def start_bot():
    bot.run(TOKEN)
