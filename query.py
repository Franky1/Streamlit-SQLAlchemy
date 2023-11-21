from utils import database


def main():
    session = database.get_database_session()
    posts = database.get_all_posts_sorted_asc(session=session)
    for post in posts:
        print(post.created, post.author, ':', post.title)


if __name__ == "__main__":
    main()
