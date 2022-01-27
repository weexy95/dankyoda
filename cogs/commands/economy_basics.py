import discord
import random

from discord.ext import commands
from utils import economy, colors, startup


config = startup.get_config()
currency_name = config['economy']['currency_name']


class EconomyBasics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='balance', aliases=['bal'], help="Get your/user's balance", usage="[user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def balance(self, ctx, user: discord.Member = None):
        checker = economy.EconomyUser(ctx.author)
        if checker.banned:
            return
        
        if user is None:
            user = ctx.author
        
        person = economy.EconomyUser(user)

        em = discord.Embed(
            title=f"{user.display_name}'s balance",
            color=colors.l_yellow
        )
        em.add_field(
            name="Wallet",
            value=str(person.wallet) + " ⬢"
        )
        em.add_field(
            name="Bank",
            value=str(person.bank) + " ⬢"
        )

        await ctx.reply(embed=em, mention_author=False)


    @commands.command(name='give', aliases=['share'], help=f"Share your {currency_name} with your friends", usage="<user> <amount>")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def share_coins(self, ctx, user: discord.Member, amount: int):
        giver = economy.EconomyUser(ctx.author)
        receiver = economy.EconomyUser(user)

        if giver.banned:
            return
        
        if user == ctx.author:
            await ctx.reply(f"You cannot share {currency_name} with your self. Buzz off, go get some friends", mention_author=False)
            return

        if amount < 0:
            await ctx.reply(f"You cannot send negative money to someone, what are you even trying?", mention_author=False)
            return

        if giver.wallet < amount:
            await ctx.reply(f"You dont have that many {currency_name} Know your place, peasant", mention_author=False)
            return

        giver.update_balance(wallet=(-amount))
        receiver.update_balance(wallet=amount)

        em = discord.Embed(
            title=f"You gave {user.display_name} {amount} ⬢",
            description=f"Now they've got `{receiver.wallet + amount} ⬢`\nand you have `{giver.wallet - amount} ⬢`",
            color=colors.l_yellow
        )
        await ctx.reply(embed=em, mention_author=False)


    @commands.command(name='rob', aliases=['steal'], help=f"Rob some {currency_name} from someone", usage="<user>")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def rob(self, ctx, user: discord.Member):
        robber = economy.EconomyUser(ctx.author)
        robee = economy.EconomyUser(user)

        if robber.banned:
            return

        if robber.wallet < 1000:
            await ctx.reply("You need atleast 1000 ⬢ in order to rob someone. How are you gonna bribe the neighbours to keep their mouths shut?")
            return
        
        if user == ctx.author:
            await ctx.reply("You must be crazy if you're trying to rob yourself.", mention_author=False)
            return

        if user.bot:
            await ctx.reply("Hey! You think it's cool to rob from poor helpless bots?", mention_author=False)
            return

        if robee.passive:
            await ctx.reply("That monk is in passive mode. Leave him alone.", mention_author=False)
            return

        if robee.wallet < 500:
            await ctx.reply(f"They're too poor. You should give them {currency_name}", mention_author=False)
            return

        chances = random.randint(1, 100)

        if chances < 35:
            percent_stolen = random.randint(20, 100)
            amount = round((percent_stolen * robee.wallet)/100)

            if amount < 500:
                amount = 500

            em = discord.Embed(
                title=f"You stole {percent_stolen}% of {user.display_name}'s {currency_name}",
                description=f"You now have `{robber.wallet + amount} ⬢` and {user.display_name} has `{robee.wallet - amount} ⬢`"
            )
            await ctx.reply(embed=em, mention_author=False)

            robber.update_balance(wallet=amount)
            robee.update_balance(wallet=(-amount))
            return

        elif 35 < chances < 50:
            em = discord.Embed(
                description=f"The neighbour's dog started barking at you and you tried to flee. But given how clumsy you are, you dropped your wallet. Classic {ctx.author.display_name} move."
            )
            await ctx.reply(embed=em, mention_author=False)
            robber.update_balance(wallet=(-robber.wallet))

        else:
            percent_stolen = random.randint(20, 100)
            amount = round((percent_stolen * robee.wallet) / 100)

            if amount < 500:
                amount = 500

            em = discord.Embed(
                description=f"You entered {user.display_name}'s house and tried to rob them but they beat the shit out of you and you had to pay them {amount} ⬢ in order to get away. Sucks to be you LOL"
            )
            await ctx.reply(embed=em, mention_author=False)
            robber.update_balance(wallet=(-amount))
            robee.update_balance(wallet=amount)


    @commands.command(name='deposit', aliases=['dep'], help=f"Deposit your precious {currency_name} in the bank", usage="[amount]")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def deposit(self, ctx, amount: int = None):
        user = economy.EconomyUser(ctx.author)
        if user.banned:
            return

        if amount is None:
            amount = user.wallet

        if amount < 0:
            await ctx.reply("What? No. Don't confuse me like that")
            return

        if amount > user.wallet:
            amount = user.wallet

        user.update_balance(wallet=(-amount), bank=amount)
        em = discord.Embed(
            title="Deposited your money in the bank",
            description=f"**Your wallet balance**: {user.wallet - amount} ⬢\n**Your bank balance**: {user.bank + amount} ⬢"
        )
        await ctx.reply(embed=em, mention_author=False)


    @commands.command(name='withdraw', aliases=['with'], help=f"Withdraw your {currency_name} from the bank", usage="[amount]")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def withdraw(self, ctx, amount: int = None):
        user = economy.EconomyUser(ctx.author)
        if user.banned:
            return

        if amount is None:
            amount = user.bank

        if amount < 0:
            await ctx.reply("What? No. Don't confuse me like that")
            return

        if amount > user.bank:
            amount = user.bank

        user.update_balance(wallet=amount, bank=(-amount))
        em = discord.Embed(
            title="Withdrawn your money in the bank",
            description=f"**Your wallet balance**: {user.wallet + amount} ⬢\n**Your bank balance**: {user.bank - amount} ⬢"
        )
        await ctx.reply(embed=em, mention_author=False)

def setup(bot):
    bot.add_cog(EconomyBasics(bot))