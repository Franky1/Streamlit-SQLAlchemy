import time

from utils import database2 as database	 # changed from database to database2


def main():
    db = database.get_database()
    database.connect(db)
    database.clear_table(db)
    for _ in range(10):
        database.generate_fake_post(db)
        time.sleep(0.1)
    database.disconnect(db)


if __name__ == "__main__":
    main()
