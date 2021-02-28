from discord.ext import commands
from discord_bot.player_value import find_value, similar_value

from discord_bot.combine import get_combine_results
from discord_bot.snaps import get_snap_counts
from discord_bot.weekly_stats import get_weekly_stats, get_player_stat
from discord_bot.card_check import get_injured_starters
from discord_bot.roster_analysis import get_roster_ages, get_roster_value


class MiscCommands(commands.Cog):
    """Commands for trades"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong')

    @commands.command()
    async def combine(self, ctx, player_name):
        await ctx.send(get_combine_results(player_name))

    @commands.command(
        help="Checks sleeper starting lineups for injured players. Does not factor in bye weeks yet",
        brief="Checks starting lineups are eligible.")
    async def cardcheck(self, ctx):
        await ctx.send(get_injured_starters())

    @commands.command()
    async def stat(self, ctx, name, stat_name):
        await ctx.send(get_player_stat(name, stat_name))

    @commands.command()
    async def snaps(self, ctx, player_name):
        await ctx.send(get_snap_counts(player_name))

    @commands.command()
    async def roster_ages(self, ctx):
        await ctx.send(get_roster_ages())

    @commands.command()
    async def roster_value(self, ctx):
        await ctx.send(get_roster_value())

    @commands.command()
    async def week(self, ctx, nfl_season, nfl_week, player_name):
        await ctx.send(get_weekly_stats(player_name, nfl_week))
