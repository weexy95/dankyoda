import discord
import psycopg2

from db import *


class EconomyUser:
    def __init__(self, user: discord.User, ctx):
        self.info = self.userinfo(user.id)

        self.user = user
        self.ctx = ctx
        self.wallet = round(self.get_wallet())
        self.bank = round(self.get_bank())
        self.level = round(self.get_level())
        self.passive = round(self.get_passive_status())
        self.banned = round(self.get_ban_status())
        self.mentions = False


    def userinfo(self, userid) -> dict:
        data = {}

        db.execute(f"SELECT * FROM userdata WHERE user_id = '{userid}';")
        info = get_all_data(db)

        data['wallet'] = info[0]
        data['bank'] = info[1]
        data['level'] = info[2]
        data['passive'] = info[3]
        data['is_banned'] = info[4]

        print(f"type - {type(info[0])} \ndata: {info[0]}")

        if info is None:
            new_acc = self.create_account()
            if new_acc:
                return self.userinfo(userid)

        return data

    def create_account(self):
        try:
            db.execute(f"INSERT INTO userdata(user_id, wallet, bank, level, passive, is_banned) VALUES('{self.user.id}', 500, 0, 0, False, False)")
            database.commit()
            return True
        except Exception as e:
            if "already exists" in e:
                return True
            else:
                return False


    def get_wallet(self) -> int:
        db.execute(f"SELECT wallet FROM userdata WHERE user_id = '{self.user.id}'")
        wallet = get_data(db)

        if wallet is None:
            self.create_account()
            return 500

        return int(wallet)


    def get_bank(self) -> int:
        db.execute(f"SELECT bank FROM userdata WHERE user_id = '{self.user.id}'")
        bank = get_data(db)

        if bank is None:
            self.create_account()
            return 0

        return int(bank)


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

        if status == "True":
            return True
        else:
            return False


    def get_ban_status(self) -> bool:
        db.execute(f"SELECT is_banned FROM userdata WHERE user_id = '{self.user.id}'")
        status = get_data(db)

        if status is None:
            self.create_account()
            return False

        if status == "True":
            return True
        else:
            return False


    def update_balance(self, wallet: int = None, bank: int = None):
        try:
            if wallet:
                db.execute(f"UPDATE userdata SET wallet = {self.wallet + wallet} WHERE user_id = '{self.user.id}'")
            if bank:
                db.execute(f"UPDATE userdata SET bank = {self.bank + bank} WHERE user_id = '{self.user.id}'")
            database.commit()
            return True

        except psycopg2.Error or psycopg2.DatabaseError as e:
            try:
                self.create_account()
                if wallet:
                    db.execute(f"UPDATE userdata SET wallet = {self.wallet + wallet} WHERE user_id = '{self.user.id}'")
                if bank:
                    db.execute(f"UPDATE userdata SET bank = {self.bank + bank} WHERE user_id = '{self.user.id}'")
                database.commit()
                return True

            except Exception as e:
                return e


    def set_balance(self, wallet: int = None, bank: int = None):
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

                if wallet:
                    db.execute(f"UPDATE userdata SET wallet = {wallet} WHERE user_id = '{self.user.id}'")
                if bank:
                    db.execute(f"UPDATE userdata SET bank = {bank} WHERE user_id = '{self.user.id}'")
                database.commit()
                return True

            except Exception as e:
                return e


    def update_level(self, new_level: int):
        try:
            db.execute(f"UPDATE userdata SET level = {new_level} WHERE user_id = '{self.user.id}'")
            database.commit()
            return True
        except psycopg2.Error or psycopg2.DatabaseError as e:
            try:
                self.create_account()
                return True
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
