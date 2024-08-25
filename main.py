
from config import config
from src.postgres_db import DBPostgres


def main():
    params = config()
    db = DBPostgres('hh_db', params)
    db.create_db()
    db.save_data_to_db()


if __name__ == "__main__":
    main()
