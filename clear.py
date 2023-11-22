from utils import database


def main():
    session = database.get_database_session()
    database.clear_table(session)
    print(database.get_post_count(session=session))


if __name__ == "__main__":
    main()
