import discord
from dotenv import load_dotenv
import urllib3
import os
import heroku3
from io import BytesIO
from discord.ext import commands
from utils import economy, colors, startup


load_dotenv()
heroku_key = os.getenv("heroku_key")
urllib3.disable_warnings()


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = startup.get_config()
        self.heroku_ = heroku3.from_key(heroku_key)

    @commands.is_owner()
    @commands.command(name="botlog", aliases=["heroku-log"], usage="[lines]", help="Get bot logs - errors, warning, messages, etc.", description="Get the logs of the discord bot. If the number of lines is not defined then it defaults to 25 lines of most recent logs")
    async def botlog(self, ctx, lines: int = 0):
        if lines == 0:
            lines = 25

        logs = self.heroku_.get_app_log("dank-yoda", lines=lines)
        as_bytes = map(str.encode, logs)
        content = b"".join(as_bytes)

        if len(logs) < 1900:
            await ctx.author.send(embed=discord.Embed(
                description=f"Last {lines} lines of log by the bot from heroku app `dank-yoda`",
                color=discord.Color.purple()
            ), content=f'''```accesslog
{logs}```''')
        else:
            await ctx.author.send(embed=discord.Embed(
                description=f"Last {lines} lines of log by the bot from heroku app `dank-yoda`",
                color=discord.Color.purple()
            ), file=discord.File(BytesIO(content), "logs.log"))

        await ctx.send(embed=discord.Embed(
            description="<:flux_check:934693030592655411> I have sent you a private message!",
            color=discord.Color.brand_green()
        ))

    @commands.is_owner()
    @commands.command(name="speak", aliases=["echo"], help="Send a normal message via the bot...")
    async def say(self, ctx, *, args):
        if ctx.message.author.id in self.client.owner_ids:
            await ctx.send(args)
        else:
            return

    @commands.is_owner()
    @commands.command(name="reboot", aliases=['restart'], help="Stops the bot and starts it again...",)
    async def shutdown(self, ctx):
        async def view_timeout():
            timeup_embed = discord.Embed(
                description="Welp! fine not doing that"
            )
            await choices.edit(embed=timeup_embed, view=None)
            await choices.delete(delay=5)
            return

        async def cancel_click(interaction):
            if interaction.user.guild_permissions.administrator:
                await interaction.message.edit(
                    embed=discord.Embed(description=f"Cancelled bot restart!", colour=discord.Colour.brand_green()),
                    view=None)
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
                heroku_ = heroku3.from_key(os.getenv("heroku_key"))
                flux_app = heroku_.apps()['dank-yoda']
                flux_app.restart()
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


def setup(bot):
    bot.add_cog(Owner(bot))
