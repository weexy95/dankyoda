import discord

from discord.ext import commands
from utils import economy, colors, startup


config = startup.get_config()
currency = config['economy']['currency']


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='balance', aliases=['bal'], help="Get your/user's balance", usage="[user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def balance(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        person = economy.EconomyUser(user)

        em = discord.Embed(
            title=f"{user.display_name}'s balance",
            color=colors.l_yellow
        )
        em.add_field(
            name="Wallet",
            value=person.wallet
        )
        em.add_field(
            name="Bank",
            value=person.bank
        )

        await ctx.reply(embed=em, mention_author=False)


    @commands.command(name='give', aliases=['share'], help=f"Share your {currency} with your friends", usage="<user> <amount>")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def share_coins(self, ctx, user: discord.Member, amount: int):
        if user == ctx.author:
            await ctx.reply(f"You cannot share {currency} with your self. Buzz off, go get some friends", mention_author=False)
            return

        if amount < 0:
            await ctx.reply(f"You cannot send negative money to someone, what are you even trying?", mention_author=False)
            return

        giver = economy.EconomyUser(ctx.author)
        receiver = economy.EconomyUser(user)

        giver.update_status('is_banned', False)

        if receiver.get_ban_status() == True:
            return

        if giver.wallet < amount:
            await ctx.reply("Know your place, peasant", mention_author=False)
            return





def setup(bot):
    bot.add_cog(Economy(bot))
