from prisma_client import Prisma


def get_database():
    db = Prisma()
    return db


def get_all_posts(db):
    posts = db.post.find_many()
    return posts


def get_all_posts_sorted(db, by="created_at", order="desc"):
    posts = db.post.find_many(order={by: order})
    return posts


def get_single_post(db, post_id):
    post = db.post.find_first(where={"id": post_id})
    return post


if __name__ == "__main__":
    db = get_database()
    db.connect()
    posts = get_all_posts_sorted(db, by="author", order="asc")
    for post in posts:
        print(post.created_at, post.author, ':', post.title)
    db.disconnect()
