import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DATABASE_URL")

database = psycopg2.connect(db_url)
print("Opened database successfully")


def get_data(db):
    """
    Almost same as db.fetchone()
    """
    for row in db:
        return row[0]

def get_all_data(db):
    """
    Almost same as db.detchall()
    """
    lst = []
    for tup in db:
        lst.append(tup[0])

    return lst


db = database.cursor()
database.commit()
