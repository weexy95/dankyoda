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

	for cog in os.listdir("cogs/commands"):
		if cog.endswith(".py"):
			if cog[:-3] in blacklisted_cogs:
				colored(242, 203, 125, f"Skipped cog: {cog}")
			else:
				try:
					bot.load_extension(f"cogs.commands.{cog[:-3]}")
					print(f"Loaded cog: {cog[:-3]}")
				except Exception as e:
					exception = f"{type(e).__name__}: {e}"
					colored(255, 62, 62, f"Failed to load cog: cogs/commands/{cog}\n{exception}")



def load_events(bot):
	blacklisted_cogs = []

	for cog in os.listdir("cogs/events"):
		if cog.endswith(".py"):
			if cog[:-3] in blacklisted_cogs:
				colored(242, 203, 125, f"Skipped cog: {cog}")
			else:
				try:
					bot.load_extension(f"cogs.events.{cog[:-3]}")
					print(f"Loaded cog: {cog[:-3]}")
				except Exception as e:
					exception = f"{type(e).__name__}: {e}"
					colored(255, 62, 62, f"Failed to load cog: cogs/events/{cog}\n{exception}")
