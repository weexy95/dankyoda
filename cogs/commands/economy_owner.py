import discord

from discord.ext import commands
from utils import economy


class Economy_owner(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.group(name="economyeval", invoke_without_command=True)
    @commands.is_owner()
    async def economy_eval(self, ctx):
        await ctx.reply("Commands:\ncreate_account\nget_wallet\nget_bank\nget_level\nget_passive_status\nget_ban_status\nupdate_balance\nupdate_level\nupdate_status")

    @economy_eval.command(name='create_account')
    async def create_account(self, ctx, user: discord.User):
        user = economy.EconomyUser(user)
        await ctx.reply(user.create_account())

    @economy_eval.command(name="get_wallet")
    async def get_wallet(self, ctx, user: discord.User):
        user = economy.EconomyUser(user)
        await ctx.reply(user.wallet)

    @economy_eval.command(name="get_bank")
    async def get_bank(self, ctx, user: discord.User):
        user = economy.EconomyUser(user)
        await ctx.reply(user.bank)

    @economy_eval.command(name="get_level")
    async def get_level(self, ctx, user: discord.User):
        user = economy.EconomyUser(user)
        await ctx.reply(user.level)

    @economy_eval.command(name="get_passsive_status")
    async def get_passive_status(self, ctx, user: discord.User):
        user = economy.EconomyUser(user)
        await ctx.reply(user.passive)

    @economy_eval.command(name="get_ban_status")
    async def get_ban_status(self, ctx, user: discord.User):
        user = economy.EconomyUser(user)
        await ctx.reply(user.banned)

    @economy_eval.command(name="update_balance")
    async def update_balance(self, ctx, user: discord.User, wallet: int = 0, bank: int = 0):
        user = economy.EconomyUser(user)
        await ctx.reply(user.update_balance(wallet=wallet, bank=bank))

    @economy_eval.command(name="update_level")
    async def update_level(self, ctx, user: discord.User, level: int):
        user = economy.EconomyUser(user)
        await ctx.reply(user.update_level(level))

    @economy_eval.command(name="update_status")
    async def update_status(self, ctx, user: discord.User, status_of, new_status: bool):
        user = economy.EconomyUser(user)
        await ctx.reply(user.update_status(status_of=status_of, new_status=new_status))


def setup(bot):
    bot.add_cog(Economy_owner(bot))
