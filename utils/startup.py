import os
import sys
import json
import discord

from utils.colors import *


def get_config():
	if not os.path.isfile("config.json"):
		sys.exit("'config.json' not found! Please add it and try again.")

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
	for file in os.listdir("cogs/events/"):
		if file.endswith(".py"):
			extension = file[:-3]
			blacklisted_ext = []
			blacklisted_ext = ["on_command_error"]

			if extension in blacklisted_ext:
				print(f"{t_yellow}Skipped event: {extension}{t_white}")

			else:
				try:
					bot.load_extension(f"cogs.events.{extension}")
					print(f"Loaded event: {extension}")

				except Exception as e:
					exception = f"{type(e).__name__}: {e}"
					print(f"{t_red}Failed to load event {extension}\n{exception}{t_white}")
