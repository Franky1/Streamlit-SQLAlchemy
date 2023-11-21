import random
import time

from faker import Faker
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, func, text, select

from utils import avatar
from utils.models import Base, Post


Faker.seed(random.randint(1, 1_000_000))
fake = Faker(locale="en_US")


def get_database_session():
    engine = create_engine("sqlite+pysqlite:///posts.sqlite", echo=False)
    Base.metadata.create_all(bind=engine)
    session = Session(bind=engine)
    return session


# def connect(db):
#     if not db.is_connected():
#         db.connect()


# def disconnect(db):
#     if db.is_connected():
#         db.disconnect()


def clear_table(session):
    with session.begin():
        session.execute(text("DELETE FROM Post"))


def get_all_posts(session):
    posts = session.query(Post).all()
    return posts


def get_all_posts_sorted_desc(session, by="created"):
    posts = session.query(Post).order_by(getattr(Post, by).desc()).all()
    return posts


def get_all_posts_sorted_asc(session, by="created"):
    posts = session.query(Post).order_by(getattr(Post, by).asc()).all()
    return posts


def get_single_post(session, uuid):
    post = session.get(Post, uuid)
    return post


def generate_fake_post(session):
    author = f"{fake.first_name()} {fake.last_name()}"
    post = Post(
        title=fake.sentence(nb_words=7).strip("."),
        content=fake.paragraph(nb_sentences=40),
        author=author,
        avatar=avatar.generate_circular_thumbnail_bytes(string=author),
    )
    with session.begin():
        session.add(post)


def delete_post(session, uuid=None):
    if uuid:
        with session.begin():
            session.query(Post).filter(Post.uuid == uuid).delete()


def get_oldest_post(session):
    post = session.query(Post).order_by(Post.created.asc()).first()
    return post


def get_newest_post(session):
    post = session.query(Post).order_by(Post.created.desc()).first()
    return post


def get_random_post(session):
    post = session.query(Post).order_by(func.random()).first()
    return post


def get_post_count(session):
    count = session.scalar(select(func.count(Post.uuid)))
    return count


def main():
    session = get_database_session()
    clear_table(session)
    for _ in range(10):
        generate_fake_post(session)
        time.sleep(0.1)
    print(get_post_count(session))


if __name__ == "__main__":
    main()
