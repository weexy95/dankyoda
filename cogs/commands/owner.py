import discord
import urllib3
import os
import heroku3

from dotenv import load_dotenv
from io import BytesIO
from discord.ext import commands
from utils import colors, economy, startup


load_dotenv()
heroku_key = os.getenv("HEROKU_API_KEY")
urllib3.disable_warnings()


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = startup.get_config()
        self.heroku_ = heroku3.from_key(heroku_key)

    @commands.group(name="cval", help="eval, but lol its for - currency", invoke_without_command=True)
    @commands.is_owner()
    async def economy_eval(self, ctx):
        await ctx.reply("Commands:\ncreate_account\nget_wallet\nget_bank\nget_level\nget_passive_status\nget_ban_status\nset_balance\nupdate_balance\nupdate_level\nupdate_status")

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

    @economy_eval.command(name="set_balance")
    async def set_balance(self, ctx, user: discord.User, wallet: int = None, bank: int = None):
        user = economy.EconomyUser(user)
        await ctx.reply(user.set_balance(wallet=wallet, bank=bank))

    @economy_eval.command(name="update_level")
    async def update_level(self, ctx, user: discord.User, level: int):
        user = economy.EconomyUser(user)
        await ctx.reply(user.update_level(level))

    @economy_eval.command(name="update_status")
    async def update_status(self, ctx, user: discord.User, status_of, new_status: bool):
        user = economy.EconomyUser(user)
        await ctx.reply(user.update_status(status_of=status_of, new_status=new_status))


    @commands.command(name="botlog", aliases=["heroku-log"], usage="[lines]", help="Get bot logs - errors, warning, messages, etc.", description="Get the logs of the discord bot. If the number of lines is not defined then it defaults to 25 lines of most recent logs")
    @commands.is_owner()
    async def botlog(self, ctx, lines: int = 25):
        logs = self.heroku_.get_app_log("dank-yoda", lines=lines)
        as_bytes = map(str.encode, logs)
        content = b"".join(as_bytes)

        if len(logs) < 1900:
            await ctx.author.send(
                embed=discord.Embed(
                    description=f"Last {lines} lines of log by the bot from heroku app `dank-yoda`",
                    color=discord.Color.purple()
                ),
                content=f'''```accesslog{logs}```'''
            )

        else:
            await ctx.author.send(
                embed=discord.Embed(
                    description=f"Last {lines} lines of log by the bot from heroku app `dank-yoda`",
                    color=discord.Color.purple()
                ),
                file=discord.File(BytesIO(content), "logs.log")
            )

        await ctx.send(
            embed=discord.Embed(
                description="<:flux_check:934693030592655411> I have sent you a private message!",
                color=discord.Color.brand_green()
            )
        )

    @commands.command(name="speak", aliases=["echo"], usage= "<args>", help="Send a normal message via the bot")
    @commands.is_owner()
    async def say(self, ctx, *, args):
        if ctx.message.author.id in self.client.owner_ids:
            await ctx.send(args)
        else:
            return


    @commands.command(name="reboot", aliases=['restart'], usage="", help="Stops the bot and starts it again")
    @commands.is_owner()
    async def reboot(self, ctx):
        async def view_timeout():
            timeup_embed = discord.Embed(description="Welp! fine not doing that")
            await choices.edit(embed=timeup_embed, view=None)
            await choices.delete(delay=5)
            return

        async def cancel_click(interaction):
            if interaction.user.guild_permissions.administrator:
                await interaction.message.edit(
                    embed=discord.Embed(description=f"Cancelled bot restart!", colour=discord.Colour.brand_green()),
                    view=None
                )
                await choices.delete(delay=5)
                view.stop()
                return

            else:
                pass

        async def ok_click(interaction):
            if interaction.user == ctx.author:
                embed = discord.Embed(
                    description="Restarting the bot! This may take a few seconds....",
                    color=0x42F56C
                )
                await ctx.send(embed=embed)

                heroku = heroku3.from_key(os.getenv("HEROKU_API_KEY"))

                dankyoda = heroku.apps()['dank-yoda']
                dankyoda.restart()

            else:
                pass

        view = discord.ui.View(timeout=15)

        ok_butt = discord.ui.Button(label="Restart!", style=discord.ButtonStyle.green)
        ok_butt.callback = ok_click

        view.add_item(ok_butt)

        cancel_butt = discord.ui.Button(label="Cancel!", style=discord.ButtonStyle.danger)
        cancel_butt.callback = cancel_click

        view.add_item(cancel_butt)
        view.on_timeout = view_timeout

        confirmation = discord.Embed(
            description=f"Are you sure you want to restart the bot?",
            color=0xF59E42
        )
        choices = await ctx.send(embed=confirmation, view=view)

    @commands.command(name='reload')
    @commands.is_owner()
    async def reload_cog(self, ctx, cog):
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            self.bot.load_extension(f"cogs.{cog}")

            em = discord.Embed(
                title="Cog Reloaded",
                description=f"cogs.{cog}",
                color=colors.l_red
            )
            await ctx.reply(embed=em)
        except Exception as e:
            em = discord.Embed(
                title="Error!",
                description=f"```{e}```",
                color=colors.l_red
            )
            await ctx.reply(embed=em)

    @commands.command(name='load')
    @commands.is_owner()
    async def load_cog(self, ctx, cog):
        try:
            self.bot.load_extension(f"cogs.{cog}")

            em = discord.Embed(
                title="Cog Loaded",
                description=f"cogs.{cog}",
                color=colors.l_red
            )
            await ctx.reply(embed=em)
        except Exception as e:
            em = discord.Embed(
                title="Error!",
                description=f"```{e}```",
                color=colors.l_red
            )
            await ctx.reply(embed=em)

    @commands.command(name='unload')
    @commands.is_owner()
    async def unload_cog(self, ctx, cog):
        try:
            self.bot.unload_extension(f"cogs.{cog}")

            em = discord.Embed(
                title="Cog unloaded",
                description=f"cogs.{cog}",
                color=colors.l_red
            )
            await ctx.reply(embed=em)
        except Exception as e:
            em = discord.Embed(
                title="Error!",
                description=f"```{e}```",
                color=colors.l_red
            )
            await ctx.reply(embed=em)

def setup(bot):
    bot.add_cog(Owner(bot))
