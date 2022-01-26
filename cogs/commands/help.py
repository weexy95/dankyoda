import discord
from cogs.cog_helpers.pages import Paginator
from discord.ext import commands
from discord.ext.commands import Cog, slash_command
from discord.ui import Select, View
from db import *


def check_field(ctx, cog, bot):
	cog = cog.lower()
	if cog == "owner":
		if ctx.author.id not in bot.owner_ids:
			return False
	return True


def get_working_cogs(ctx, bot):
	cogs = []
	for cog in os.listdir("cogs/commands/"):
		if os.path.isdir(f"cogs/commands/{cog}"):
			if cog != "__pycache__":
				if len(os.listdir(f"cogs/commands/{cog}")) != 0:
					if check_field(ctx, cog, bot):
						cogs.append(cog)
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


class Help(Cog):
	def __init__(self, bot):
		self.bot = bot


	def get_all_command(self):
		aliases = {}
		for command in self.bot.commands:
			aliases[f'{command}'] = str(command)
			for i in command.aliases:
				aliases[f'{i}'] = str(command)
		return aliases

	@commands.command(name="help", aliases=['h'], usage="[command/category]", help="Get help on a command or the Bot!")
	@slash_command()
	async def help(self, ctx, *, command_name=''):
		working_cogs = get_working_cogs(ctx, self.bot)

		if command_name.lower() in self.get_all_command():
			command_name = self.get_all_command()[f"{command_name}"]
			command = discord.utils.get(self.bot.commands, name=command_name)
			await cmd_help(ctx, command)
			return

		# A custom url for when a user clicks on a command
		url = "https://www.google.com"

		all_page_description = f'**Available command Categories -**\n\n'

		for x in working_cogs:
			all_page_description = all_page_description + f"● **{x.capitalize()}**\n"

		all_page_description += "\n Select command category below for more details.."

		all_page = discord.Embed(
			description=all_page_description,
			color=0xf2cb7d,
		)


		async def my_select_view_timeout():
			my_select.disabled = True
			await message.edit(view=my_select_view)

		my_select_view = View(timeout=20)
		my_select_view.on_timeout = my_select_view_timeout
		select_options = {}

		for i in range(len(working_cogs)):
			select_options[str(i)] = working_cogs[i]


		def index_commands(value):
			command_list = []
			for cmd_name in os.listdir(f"cogs/commands/{value.lower()}/"):
				if cmd_name.endswith(".py"):
					cmd = self.bot.get_command(name=cmd_name[:-3])

					if cmd is None:
						continue

					cmd_help = cmd.help

					if cmd_help is None:
						cmd_help = "No help text provided by developer"

					command_list.append([str(cmd), cmd_help])
			return command_list

		async def paginate(ctx, commands, value):
			pages = []
			index = 0

			while True:
				description = ''

				for z in range(0, 7):
					try:
						description = description + f"\n **[{commands[index][0]}]({url})**\n<:reply:928546470662119444>{commands[index][1]}"
						index += 1
					except IndexError:
						break

				try:
					page = discord.Embed(
						title=f"{value.capitalize()} commands: ",
						description=description
					)
					pages.append(page)

				except IndexError:
					page = discord.Embed(title=f"{value.capitalize()} commands: ", description=description)
					pages.append(page)
					break

			paginator = Paginator(
				pages=pages,
				show_disabled=True,
				show_indicator=True,
				disable_on_timeout=True,
				timeout=18,
				custom_view=my_select_view
			)
			paginator.customize_button(
				button_name="prev",
				button_emoji="<:left:930372441249808415>",
				button_style=discord.ButtonStyle.primary
			)
			paginator.customize_button(
				button_name="next",
				button_emoji="<:right:930372441220472863>",
				button_style=discord.ButtonStyle.primary
			)

			await paginator.edit(ctx, message=message)


		async def my_select_callback(interaction):
			value_index = my_select.values[0]
			value = select_options[str(value_index)].lower()

			my_select.placeholder = value.capitalize()

			if my_select.values[0] == 'x':
				await interaction.message.edit(embed=all_page, view=my_select_view)
				return

			command_list = index_commands(value)

			if len(command_list) > 7:
				await paginate(ctx, command_list, value)

			else:
				description = ''

				for x in range(len(command_list)):
					description = description + f"\n **[{command_list[x][0]}]({url})**\n<:reply:928546470662119444>{command_list[x][1]}"

				page = discord.Embed(title=f"{value.capitalize()} commands -", description=description)

				await interaction.message.edit(embed=page, view=my_select_view)

		my_select = Select(
			min_values=1,
			max_values=1,
			placeholder="Select Command Category"
		)

		for i in select_options.keys():
			my_select.add_option(label=select_options[i].capitalize(), value=str(i))

		my_select.callback = my_select_callback
		my_select_view.add_item(my_select)

		if command_name == "" or command_name is None:
			message = await ctx.send(embed=all_page, view=my_select_view)

		elif command_name.lower() in working_cogs:
			my_select_view.placeholder = f"{command_name.capitalize()}"
			category_cmd_list = index_commands(command_name.lower())
			des = ''

			for x in range(len(category_cmd_list)):
				des = des + f"\n **[{category_cmd_list[x][0]}]({url})**\n<:reply:928546470662119444>{category_cmd_list[x][1]}"

			page = discord.Embed(title=f"{command_name.capitalize()} commands -", description=des)
			message = await ctx.send(embed=page, view=my_select_view)

		elif len(command_name) > 0 and command_name.lower() not in self.get_all_command():
			message = await ctx.send(embed=all_page, view=my_select_view)


def setup(bot):
	bot.add_cog(Help(bot))
