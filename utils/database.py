import random
import sys

from faker import Faker
from sqlalchemy import create_engine, func, select, text
from sqlalchemy.orm import Session, sessionmaker

from utils.models import Base, Post

if sys.platform.startswith('win'):
    from utils import avatar
else:
    from utils import avatar2 as avatar

Faker.seed(random.randint(1, 1_000_000))
fake = Faker(locale="en_US")


def get_database_session() -> Session:
    engine = create_engine("sqlite+pysqlite:///posts.sqlite", echo=False)
    Base.metadata.create_all(bind=engine)
    Sess = sessionmaker(bind=engine)
    session = Sess()
    return session


def clear_table(session: Session):
    session.execute(text("DELETE FROM Post"))
    session.commit()


def get_all_posts(session: Session):
    posts = session.query(Post).all()
    return posts


def get_all_posts_sorted_desc(session: Session, by: str="created"):
    posts = session.query(Post).order_by(getattr(Post, by).desc()).all()
    return posts


def get_all_posts_sorted_asc(session: Session, by: str="created"):
    posts = session.query(Post).order_by(getattr(Post, by).asc()).all()
    return posts


def get_single_post(session: Session, id: int):
    post = session.get(Post, id)
    return post


def generate_fake_post(session: Session):
    author = f"{fake.first_name()} {fake.last_name()}"
    post = Post(
        title=fake.sentence(nb_words=7).strip("."),
        content=fake.paragraph(nb_sentences=40),
        author=author,
        avatar=avatar.generate_thumbnail_bytes(string=author, size=128),
    )
    session.add(post)
    session.commit()


def delete_post(session: Session, id: int=None):
    if id:
        session.query(Post).filter(Post.id == id).delete()
        session.commit()


def get_oldest_post(session: Session):
    post = session.query(Post).order_by(Post.created.asc()).first()
    return post


def get_newest_post(session: Session):
    post = session.query(Post).order_by(Post.created.desc()).first()
    return post


def get_random_post(session: Session):
    post = session.query(Post).order_by(func.random()).first()
    return post


def get_post_count(session: Session):
    count = session.scalar(select(func.count(Post.id)))
    return count


def main():
    session = get_database_session()
    clear_table(session)
    for _ in range(30):
        generate_fake_post(session)
    print(get_post_count(session))


if __name__ == "__main__":
    main()
