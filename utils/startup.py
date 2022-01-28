import os
import json
import traceback

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

	for cog in os.listdir(commands_dir):
		if cog.endswith(".py"):
			cog = cog[:-3]
		else:
			continue

		if cog in blacklisted_cogs:
			print(f"{t_yellow}Skipped cog: {cog} {t_blue}")
		else:
			try:
				bot.load_extension(f"{commands_dir.replace('/', '.')}{cog}")
				print(f"{t_blue}Loaded command cog:{t_green} {cog}{t_blue}")
			except Exception as e:
				exception = f"{type(e).__name__}: {e}"
				print(f"{t_red}Failed to load cog: cogs/commands/{cog}")
				print(f"{e}{traceback.format_exc()} {t_blue}")


def load_events(bot):
	blacklisted_cogs = []
	events_dir = "cogs/events/"

	for cog in os.listdir(events_dir):
		if cog.endswith(".py"):
			cog = cog[:-3]
		else:
			continue

		if cog in blacklisted_cogs:
			print(f"{t_yellow}Skipped event: {cog} {t_blue}")
		else:
			try:
				bot.load_extension(f"{events_dir.replace('/', '.')}{cog}")
				print(f"{t_blue}Loaded cog: {t_green}{cog}{t_blue}")
			except Exception as e:
				exception = f"{type(e).__name__}: {e}"
				print(f"{t_red}Failed to load cog: cogs/commands/{cog}\n{exception} {t_white}")
