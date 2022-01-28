import discord

from cogs.cog_helpers.pages import Paginator
from discord.ext import commands
from discord.ext.commands import Cog
from discord.ui import Select, View
from db import *
from utils.startup import get_config
from utils import colors


def check_field(ctx, cog, bot):
	cog = cog.lower()
	if cog == "owner":
		if ctx.author.id not in bot.owner_ids:
			return False
	if cog == "help":
		return False
	return True


def get_working_cogs(author, bot, auto=False):
	cogs = []
	if auto:
		for cog in os.listdir("cogs/commands/"):
			if cog.endswith(".py"):
				cog = cog[:-3]
				cog_name = cog.capitalize()
				cogs.append(cog_name)
	else:
		cogs = ["Currency", "Fun", "Bot"]
	return cogs


def decorate(command):
	if command.usage is None or command.usage == '':
		return f"```{command} {command.usage}```"
	else:
		args = []

		for key, value in command.params.items():
			if key not in ("self", "ctx"):
				if "None" in str(value) or "No reason provided" in str(value):
					args.append(f"[{key}]")
				else:
					args.append(f"<{key}>")

		args = " ".join(args)

		return f"```{command} {args}```"


async def cmd_help(ctx, command):  # Makes the embed
	aliases = f'`{command}`'

	for alias in command.aliases:
		aliases += f', `{alias}`'

	help = command.description

	if help is None:
		help = command.help

		if help is None:
			help = 'No help text provided by developer'

	em = discord.Embed(title=f"{command} info ",)

	em.add_field(name='Description:', value=f"*{help}*", inline=False)
	em.add_field(name='Usage:', value=decorate(command), inline=False)
	em.add_field(name='Aliases:', value=aliases, inline=False)
	em.set_footer(text="Usage Syntax: <required> [optional]")

	await ctx.send(embed=em)


class Bot(Cog):
	def __init__(self, bot):
		# A custom url for when a user clicks on a command - rickroll in this case
		self.url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

		self.bot = bot
		self.config = get_config()

	def get_all_command(self):
		aliases = {}
		for command in self.bot.commands:
			aliases[f'{command}'] = str(command)
			for i in command.aliases:
				aliases[f'{i}'] = str(command)
		return aliases

	@commands.command(name='ping', help="Shows the bot's ping/latency")
	async def ping(self, ctx):
		latency = round(self.bot.latency * 1000)
		if 10 < latency < 30:
			color = colors.l_green
		elif 30 < latency < 150:
			color = colors.l_yellow
		else:
			color = colors.l_red

		em = discord.Embed(
			title='Pong!',
			description=f"`{latency}`ms",
			color=color
		)
		await ctx.reply(embed=em, mention_author=False)


	@commands.command(name="help", aliases=['h'], usage="[command/category]", help="Get help on a command or the Bot!")
	async def help(self, ctx, *, command_name=''):
		working_cogs = get_working_cogs(ctx.author, self.bot)
		message = None

		if command_name.lower() in self.get_all_command():
			command_name = self.get_all_command()[f"{command_name}"]
			command = discord.utils.get(self.bot.commands, name=command_name)
			await cmd_help(ctx, command)
			return

		current_cog = working_cogs[0]

		def index_commands(value):
			command_list = []
			cog = self.bot.get_cog(value.capitalize())
			cog_commands = cog.get_commands()
			for cmd in cog_commands:
				help_cmd = cmd.help
				if help_cmd is None:
					help_cmd = "No help text provided by developer"

				command_list.append([str(cmd), help_cmd])
			return command_list

		cmd_n_help = index_commands(current_cog)
		view = View(timeout=15)

		async def view_timeout():
			for item in view.children:
				item.disabled = True
			view.stop()
			await message.edit(view=view)

		async def select_callback(interaction):
			value = my_select.values[0]

			my_select.placeholder = str(value)
			my_select.options = get_select_opts(value)

			msg_embed = build_embed(index_commands(value), value)
			if type(msg_embed) == discord.Embed:
				message = await interaction.message.edit(embed=msg_embed, view=view)
			elif type(msg_embed) == list:
				message = await paginate_(msg_embed, view, edit=True)

		def get_select_opts(present):
			s_options = []
			for x in working_cogs:
				if present == x:
					s_option = discord.SelectOption(label=x, value=x, default=True)
				else:
					s_option = discord.SelectOption(label=x, value=x)
				s_options.append(s_option)
			return s_options
		select_options = get_select_opts(current_cog)

		my_select = Select(
			placeholder=str(current_cog),
			min_values=1,
			max_values=1,
			options=select_options
		)
		my_select.callback = select_callback
		view.add_item(my_select)
		view.on_timeout = view_timeout

		def build_embed(indexed_commands, selected):
			if len(indexed_commands) < 8:
				description = f"**{selected} commands -**\n"
				for val in indexed_commands:
					c_name = val[0]
					c_help = val[1]
					description = description + f"\n**[{c_name}]({self.url})**\n<:reply:935420231185215509>{c_help}"
				embed = discord.Embed(description=description)
				return embed
			else:
				embeds = []
				description = f"**{selected} commands - **\n"
				for val in range(len(indexed_commands)):
					if val%7 == 0 and val != 0:
						embed = discord.Embed(description=description)
						embeds.append(embed)
						description = f"**{selected} commands - **\n"
					c_name = indexed_commands[val][0]
					c_help = indexed_commands[val][1]
					description = description + f"\n**[{c_name}]({self.url})**\n<:reply:935420231185215509>{c_help}"
				embeds.append(discord.Embed(description=description))
				return embeds

		async def paginate_(embeds_list, extra_view, edit=False):
			paginator = Paginator(
				pages=embeds_list,
				show_disabled=True,
				show_indicator=True,
				disable_on_timeout=True,
				timeout=18,
				custom_view=extra_view
			)
			paginator.customize_button(
				"prev",
				button_emoji="<:left:935419039122079815>",
				button_style=discord.ButtonStyle.primary
			)
			paginator.customize_button(
				"next",
				button_emoji="<:right:935419039155621888>",
				button_style=discord.ButtonStyle.primary
			)
			if edit:
				return await paginator.edit(ctx, message=message)
			else:
				return await paginator.send(ctx)

		msg_embed = build_embed(cmd_n_help, current_cog)
		if type(msg_embed) == discord.Embed:
			message = await ctx.send(embed=msg_embed, view=view)
		elif type(msg_embed) == list:
			message = await paginate_(msg_embed, view)





def setup(bot):
	bot.add_cog(Bot(bot))
