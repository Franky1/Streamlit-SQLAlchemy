import time

from utils import database


def main():
    session = database.get_database_session()
    # database.clear_table(session)
    for _ in range(10):
        database.generate_fake_post(session=session)
        time.sleep(0.1)
    print(database.get_post_count(session=session))


if __name__ == "__main__":
    main()
