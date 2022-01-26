# The code in this event is executed every time a command has been *successfully* executed

from discord.ext import commands
import json


class OnCommandCompletion(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_completion(self, ctx):
		fullCommandName = ctx.command.qualified_name
		split = fullCommandName.split(" ")
		executedCommand = str(split[0])

		print(f"Executed {executedCommand} command in {ctx.guild.name} ({ctx.guild.id}) by {ctx.author} ({ctx.author.id})")


def setup(bot):
	bot.add_cog(OnCommandCompletion(bot))
