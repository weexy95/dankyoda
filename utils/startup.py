import os
import json

from utils.colors import *


def get_config():
	if not os.path.isfile("config.json"):
		exit("'config.json' not found! Please add it and try again.")

	else:
		with open("config.json") as file:
			return json.load(file)


def load_commands(bot):
	blacklisted_cogs = []
	cogs = [
		'help',
		'economy'
	]

	for cog in cogs:
		if cog in blacklisted_cogs:
			print(f"{t_yellow}Skipped cog: {cog} {t_white}")
		else:
			try:
				bot.load_extension(f"cogs.commands.{cog}")
				print(f"Loaded cog: {cog}")
			except Exception as e:
				exception = f"{type(e).__name__}: {e}"
				print(f"{t_red}Failed to load cog: cogs/commands/{cog}\n{exception} {t_white}")


def load_events(bot):
	blacklisted_cogs = []
	cogs = [
		'on_command_completion',
		'on_command_error',
		'on_guild_join',
		'on_guild_remove',
		'on_ready'
	]

	for cog in cogs:
		if cog in blacklisted_cogs:
			print(f"{t_yellow}Skipped cog: {cog} {t_white}")
		else:
			try:
				bot.load_extension(f"cogs.commands.{cog}")
				print(f"Loaded cog: {cog}")
			except Exception as e:
				exception = f"{type(e).__name__}: {e}"
				print(f"{t_red}Failed to load cog: cogs/commands/{cog}\n{exception} {t_white}")
