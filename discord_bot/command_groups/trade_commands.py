from discord.ext import commands
from discord_bot.player_value import find_value, similar_value


class TradeCommands(commands.Cog):
    """Commands for trades"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def value(self, ctx, player_name):
        """get a player's dynasty superflex value"""
        await ctx.send(find_value(player_name))

    @commands.command()
    async def similar(self, ctx, player_name):
        """find players of similar value"""
        await ctx.send(similar_value(player_name))
