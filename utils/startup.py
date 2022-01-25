import os
import sys
import json


def get_config():
	if not os.path.isfile("config.json"):
		sys.exit("'config.json' not found! Please add it and try again.")

	else:
		with open("config.json") as file:
			return json.load(file)


def load_commands(bot):
	blacklisted_cogs = ["__pycache__"]
	blacklisted_commands = ['balance']

	for folder in os.listdir("cogs/commands/"):
		if os.path.isdir(f"cogs/commands/{folder}"):
			if folder in blacklisted_cogs:
				print(f"Skipped Command Cog: {folder}")

			for command in os.listdir(f"cogs/commands/{folder}"):
				if command.endswith(".py"):
					cmd = command[:-3]

				if cmd in blacklisted_commands:
					print(f"Skipped Command: {cmd}")
					pass

				else:
					try:
						bot.load_extension(f"cogs.commands.{folder}.{cmd}")
						print(f"Loaded command: '{cmd}'")

					except Exception as e:
						exception = f"{type(e).__name__}: {e}"
						print(f"\nFailed to load Command: {cmd} from Cog {folder}\n{exception}")


def load_events(bot):
	for file in os.listdir("cogs/events/"):
		if file.endswith(".py"):
			extension = file[:-3]
			blacklisted_ext = []
			blacklisted_ext = ["on_command_error"]

			if extension in blacklisted_ext:
				print(f"Skipped event: {extension}")

			else:
				try:
					bot.load_extension(f"cogs.events.{extension}")
					print(f"Loaded event: {extension}")

				except Exception as e:
					exception = f"{type(e).__name__}: {e}"
					print(f"\nFailed to load event {extension}\n{exception}")