import discord

from discord.ext import commands
from utils.colors import *
from utils.economy import EconomyUser
from utils.startup import get_config

config = get_config()
currency = config['economy']['currency_name']
symbol = config['economy']['currency_symbol']

class EconomyRewards(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.command(name="hourly", help="Get your free hourly rewards", usage="")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def hourly(self, ctx):
        user = EconomyUser(ctx.author)

        if user.banned:
            return

        user.update_balance(wallet=200)

        em = discord.Embed(
            title="Here are your hourly rewards",
            description=f"You received 200 ⬢"
        )
        await ctx.reply(embed=em, mention_author=False)


    @commands.command(name="daily", help="Get your free daily rewards", usage="")
    @commands.cooldown(1, 3600*24, commands.BucketType.user)
    async def daily(self, ctx):
        user = EconomyUser(ctx.author)

        if user.banned:
            return

        user.update_balance(wallet=10000)

        em = discord.Embed(
            title="Here are your hourly rewards",
            description=f"You received 10000 ⬢"
        )
        await ctx.reply(embed=em, mention_author=False)


def setup(bot):
    bot.add_cog(EconomyRewards(bot))
