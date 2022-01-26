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
	commands_dir = "cogs/commands/"

	print(f"{t_yellow} --------------------------------------------------------------------------------------- {t_white}")

	for cog in os.listdir(commands_dir):
		if cog.endswith(".py"):
			cog = cog[:-3]
		else:
			continue

		if cog in blacklisted_cogs:
			print(f"{t_yellow}Skipped cog: {cog} {t_white}")
		else:
			try:
				bot.load_extension(f"{commands_dir.replace('/', '.')}{cog}")
				print(f"Loaded command cog: {cog}")
			except Exception as e:
				exception = f"{type(e).__name__}: {e}"
				print(f"{t_red}Failed to load cog: cogs/commands/{cog}\n{exception} {t_white}")


def load_events(bot):
	blacklisted_cogs = []
	events_dir = "cogs/events/"

	print(f"{t_yellow} --------------------------------------------------------------------------------------- {t_white}")

	for cog in os.listdir(events_dir):
		if cog.endswith(".py"):
			cog = cog[:-3]
		else:
			continue

		if cog in blacklisted_cogs:
			print(f"{t_yellow}Skipped event: {cog} {t_white}")
		else:
			try:
				bot.load_extension(f"{events_dir.replace('/', '.')}{cog}")
				print(f"Loaded cog: {cog}")
			except Exception as e:
				exception = f"{type(e).__name__}: {e}"
				print(f"{t_red}Failed to load cog: cogs/commands/{cog}\n{exception} {t_white}")
