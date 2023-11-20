'''
TODO: Refactor this file to use sqlalchemy2 instead of prisma.
'''
import random
import time

from faker import Faker
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, func

from utils import avatar
from utils.models import Post


Faker.seed(random.randint(1, 1_000_000))
fake = Faker(locale="en_US")


def get_database():
    db = create_engine("sqlite:///posts.sqlite", echo=True)
    session = sessionmaker(bind=db)
    return session


def connect(db):
    if not db.is_connected():
        db.connect()


def disconnect(db):
    if db.is_connected():
        db.disconnect()


def clear_table(db):
    db.post.delete_many()


def get_all_posts(db):
    posts = db.post.find_many()
    return posts


def get_all_posts_sorted(db, by="created_at", order="desc"):
    posts = db.post.find_many(order={by: order})
    return posts


def get_single_post(db, post_id):
    post = db.post.find_first(where={"id": post_id})
    return post


def generate_fake_post(db):
    author = f"{fake.first_name()} {fake.last_name()}"
    db.post.create({
        "title": fake.sentence(nb_words=7).strip("."),
        "content": fake.paragraph(nb_sentences=40),
        "author": author,
        "avatar": avatar.generate_circular_thumbnail_bytes(string=author),
    })


def delete_post(db, post_id):
    if post_id:
        db.post.delete(where={"id": post_id})


def get_oldest_post(db):
    post = db.post.find_first(order={"created_at": "asc"})
    return post


def get_newest_post(db):
    post = db.post.find_first(order={"created_at": "desc"})
    return post


def get_random_post(db):
    post = db.query_first(
        '''
        SELECT *
        FROM post
        ORDER BY RANDOM()
        LIMIT 1
        ''',
        model = Post
    )
    return post


def get_post_count(db):
    count = db.post.count()
    return count


def main():
    db = get_database()
    db.connect()
    clear_table(db)
    for _ in range(10):
        generate_fake_post(db)
        time.sleep(0.1)
    db.disconnect()


if __name__ == "__main__":
    main()
