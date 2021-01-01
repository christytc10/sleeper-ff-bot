from discord.ext import commands
from discord_bot.player_value import find_value, similar_value


class TradeCommands(commands.Cog):
    """Commands for trades"""

    @commands.command()
    async def value(ctx, player_name):
        """get a player's dynasty superflex value"""
        await ctx.send(find_value(player_name))
