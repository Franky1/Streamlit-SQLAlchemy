import io

from PIL import Image

from utils import database


def show_image(image_byte):
    """show image with pillow"""
    image = Image.open(io.BytesIO(image_byte), formats=['PNG'])
    image.show()


def main():
    session = database.get_database_session()
    post = database.get_random_post(session=session)
    print(post.created, post.author, type(post.avatar))
    show_image(post.avatar)


if __name__ == "__main__":
    main()
