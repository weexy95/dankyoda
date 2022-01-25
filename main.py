import json
import sys

from db import *
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

"""
+------------------------------------------------+
| Defining some useful functions and variables.. |
+------------------------------------------------+
"""


def create_prefix(guild):
	db.execute(f"INSERT INTO Prefix(guild, prefix) VALUES ('{guild.id}', 'plz ')")
	print(f"Created config for new server -> {str(guild)}, ID -> {guild.id}")
	database.commit()


def get_prefix(bot, message):
	"""
	Function to get prefix for a guild
	"""
	try:
		f = open('./cache/prefix.json', 'r')
		cache = json.load(f)

		guild = str(message.guild.id)
		if guild in cache:
			prefix = commands.when_mentioned_or(cache[guild])(bot, message)
			return prefix

		else:
			db.execute(f"SELECT prefix FROM Prefix WHERE guild = '{str(message.guild.id)}'")
			prefix = db.fetchone()
			cache[str(guild)] = prefix[0]

			with open('cache/prefix.json', 'w') as f:
				json.dump(cache, f, indent=4)

			return commands.when_mentioned_or(prefix[0])(bot, message)
	except TypeError:
		create_prefix(message.guild)


def get_config():
	if not os.path.isfile("config.json"):
		# sys.exit("'config.json' not found! Please add it and try again.")
		print("FEK")
	else:
		with open("config.json") as file:
			return json.load(file)


def load_commands():
	blacklisted_cogs = ["__pycache__"]
	blacklisted_commands = []
	print("---------------------------------")
	for folder in os.listdir("cogs/commands/"):
		if os.path.isdir(f"cogs/commands/{folder}"):
			if folder in blacklisted_cogs:
				print(f"--X Skipped Command Cog : {folder}")
				continue
			for command in os.listdir(f"cogs/commands/{folder}"):
				if command.endswith(".py"):
					cmd = command[:-3]
				else:
					continue
				if cmd in blacklisted_commands:
					print(f"--X Skipped Command : {cmd}")
					pass
				else:
					try:
						bot.load_extension(f"cogs.commands.{folder}.{cmd}")
						print(f"--> Loaded command : '{cmd}'")
					except discord.ExtensionAlreadyLoaded:
						print("---------------------------------")
						continue
					except Exception as e:
						exception = f"{type(e).__name__}: {e}"
						print(f"--------------------------------------")
						print(f"Failed to load Command : {cmd} from Cog {folder}..\n Traceback - {exception}")


def load_events():
	print("---------------------------------")
	for file in os.listdir("cogs/events/"):
		if file.endswith(".py"):
			extension = file[:-3]
			blacklisted_ext = []
			blacklisted_ext = ["on_command_error"]
			if extension in blacklisted_ext:
				print(f"Skipped event : {extension}")
			else:
				try:
					bot.load_extension(f"cogs.events.{extension}")
					print(f"Loaded event  : {extension}")
				except Exception as e:
					exception = f"{type(e).__name__}: {e}"
					print(f"Failed to load event {extension}\n	{exception}")


load_dotenv()
TOKEN = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.members = True
config = get_config()

"""
+--------------------------------+
| Making the commands.Bot object |
+--------------------------------+
"""

bot = commands.Bot(
	command_prefix="plz ",
	intents=intents,
	case_insensitive=True,
	allowed_mentions=discord.AllowedMentions(everyone=False),
	owner_ids=config['owners'],
)
bot.remove_command("help")


if __name__ == '__main__':
	load_events()
	load_commands()
	if not os.path.isfile("config.json"):
		sys.exit("'config.json' not found! Please add it and try again.")
	else:
		with open("config.json") as file:
			config = json.load(file)
	prefix = config["bot_prefix"]


# Run the bot with the token
bot.run(TOKEN)
