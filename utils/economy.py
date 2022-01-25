import discord
import psycopg2

from db import *


class EconomyUser:
	def __init__(self, user: discord.User):
		self.user = user

	def create_account(self):
		db.execute(
			f"INSERT INTO userdata(user_id, wallet, bank, level, passive, is_banned) VALUES('{self.user.id}', 500, 0, 0, False, False)")
		database.commit()

	def get_wallet(self) -> int:
		db.execute(f"SELECT wallet FROM userdata WHERE user_id = '{self.user.id}'")
		wallet = get_data(db)

		if wallet is None:
			self.create_account()
			return 500

		return wallet

	def get_bank(self) -> int:
		db.execute(f"SELECT bank FROM userdata WHERE user_id = '{self.user.id}'")
		bank = get_data(db)

		if bank is None:
			self.create_account()
			return 0

		return bank

	def get_level(self) -> int:
		db.execute(f"SELECT level FROM userdata WHERE user_id = '{self.user.id}'")
		level = get_data(db)

		if level is None:
			self.create_account()
			return 0

		return level

	def get_passive_status(self) -> bool:
		db.execute(f"SELECT passive FROM userdata WHERE user_id = '{self.user.id}'")
		status = get_data(db)

		if status is None:
			self.create_account()
			return False

		return bool(status)

	def get_ban_status(self) -> bool:
		db.execute(f"SELECT is_banned FROM userdata WHERE user_id = '{self.user.id}'")
		status = get_data(db)

		if status is None:
			self.create_account()
			return False

		return bool(status)

	def update_balance(self, wallet: int = None, bank: int = None):
		try:
			if wallet:
				db.execute(f"UPDATE userdata SET wallet = {wallet} WHERE user_id = '{self.user.id}'")
			if bank:
				db.execute(f"UPDATE userdata SET bank = {bank} WHERE user_id = '{self.user.id}'")
			database.commit()
			return True

		except psycopg2.Error or psycopg2.DatabaseError as e:
			try:
				self.create_account()
			except:
				return e

	def update_level(self, new_level: int):
		try:
			db.execute(f"UPDATE userdata SET level = {new_level} WHERE user_id = '{self.user.id}'")
			database.commit()
			return True
		except psycopg2.Error or psycopg2.DatabaseError as e:
			try:
				self.create_account()
			except:
				return e

	def update_status(self, status_of, new_status: bool):
		try:
			db.execute(f"UPDATE userdata SET {status_of} = '{new_status}' WHERE user_id = '{self.user.id}'")
			database.commit()
			return True
		except psycopg2.Error or psycopg2.DatabaseError as e:
			try:
				self.create_account()
			except:
				return e
