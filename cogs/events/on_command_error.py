import hashlib
import json
import random
import traceback

from io import BytesIO
import discord
from discord.ext import commands


async def gen_code(name: str):
    return hashlib.sha256(name.encode('ascii', errors='ignore')).hexdigest()


def usage(command):
    args = []

    for key, value in command.params.items():
        if key not in ("self", "ctx"):
            if "None" in str(value) or "No reason provided" in str(value):
                args.append(f"[{key}]")
            else:
                args.append(f"<{key}>")

    args = " ".join(args)

    return f"```{command} {args}```"


class ErrorHandling(commands.Cog):
    def __init__(self, client):
        self.client = client
        with open("config.json", 'r') as config_file:
            self.config = json.load(config_file)
            config_file.close()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            em = discord.Embed(
                title='Command incomplete!',
                color=discord.Color.brand_red(),
                description=f"This command is missing some arguements.. \n\n **Usage -** {usage(ctx.command)}"
            )

            await ctx.reply(embed=em, mention_author=False)
            ctx.command.reset_cooldown(ctx)
            return


        elif isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_permissions]

            if len(missing) > 2:
                permission = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                permission = ' and '.join(missing)

            em = discord.Embed(
                title='Missing Permissions!',
                description=f"You need the `{permission}` permission to do that",
                color=discord.Color.brand_red()
            )
            await ctx.reply(embed=em, mention_author=False)
            return


        elif isinstance(error, commands.MemberNotFound):
            not_found = [
                "What are you talking about??\n\nNo such person exists on this server...",
                "I searched through the deepest places of this server and still\nI couldn't find the person you mentioned",
                "Welp, this person doesn't exist in this server."
            ]
            em = discord.Embed(
                description=random.choice(not_found),
                color=discord.Color.brand_red())

            await ctx.reply(embed=em, mention_author=False)
            ctx.command.reset_cooldown(ctx)
            return


        elif isinstance(error, commands.BotMissingPermissions):
            mp = error.missing_permissions[0]
            mp = mp.title()
            mp = mp.replace('_', ' ')

            em = discord.Embed(
                description=f"This should have worked but I have some permissions missing...\n\nMissing Permission - `{mp}`",
                color=discord.Color.brand_red())

            try:
                await ctx.send(embed=em)
                return
            except discord.Forbidden:
                await ctx.send(
                    f"I don't have the {mp} permission. F")  # In case the bot doesn't have embed links permission
            return


        elif isinstance(error, commands.CommandOnCooldown):
            mode = "second(s)"
            if error.retry_after > 120:
                error.retry_after = error.retry_after // 60
                mode = "minute(s)"

            if error.retry_after > 3600:
                error.retry_after = error.retry_after // 3600
                mode = "hour(s)"

            em = discord.Embed(
                title="Whoa there, hold your horses!",
                description=f"The `{ctx.command}` command is on a cooldown, try again in **{error.retry_after:,.1f} {mode}**",
                colour=discord.Color.brand_red()
            )
            await ctx.reply(embed=em, mention_author=False)
            return


        elif isinstance(error, commands.BadArgument):
            em = discord.Embed(
                title="Invalid arguments!", color=discord.Color.brand_red(),
                description=f"I think you used the command wrong. For more info, try running: ```plz help {ctx.command}```"
            )
            await ctx.send(embed=em)
            ctx.command.reset_cooldown(ctx)
            return


        elif isinstance(error, commands.CommandNotFound):
            return


        elif isinstance(error, discord.Forbidden):
            try:
                em = discord.Embed(
                    title='Missing Permissions',
                    description="**Error code 403 Forbidden was raised. I can't do anything here...** \n\nContact my developers or join support server for help",
                    color=discord.Color.brand_red()
                )
                ctx.reply(embed=em, mention_author=False)
                return
            except discord.Forbidden:
                await ctx.reply("I need the 'Embed Links' permission.")
                return


        else:
            if ctx.command.name.lower() == 'eval_fn':
                return

            code = await gen_code(ctx.command.name.lower())
            error = traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__)
            error = ''.join(error)

            if error.endswith('Missing Permissions'):
                try:
                    return await ctx.send(
                        'I am missing permissions inorder to run this command. I cannot identify the correct one.')
                except discord.Forbidden:
                    return

            channel = self.bot.get_channel(800315954008948747)
            if len(error) < 1850:
                await channel.send(
                    '**Error in the command {}**, Located from `{}` by user `{}`\n```\n'.format(ctx.command.name,
                                                                                                ctx.guild.name,
                                                                                                ctx.author) + error + '\n```')
            else:
                await channel.send(
                    content='**Error in the command {}**, Located from `{}` by user `{}`'.format(ctx.command.name,
                                                                                                 ctx.guild.name,
                                                                                                 ctx.author),
                    file=discord.File(fp=BytesIO(error.encode(errors='ignore')), filename='error.log')
                )

            try:
                await ctx.send(
                    '**An unknown error has occurred. It has been reported automatically!**\n**Your error code:** `{}`'.format(
                        code))
            except discord.Forbidden:
                pass


def setup(client):
    client.add_cog(ErrorHandling(client))
