import io

from avatar_generator import Avatar
from PIL import Image


def photo(string, size=64):
    avatar = Avatar.generate(size=size, string=string, filetype="PNG")
    return avatar


def show_image(image_byte):
    """show image with pillow
    """
    image = Image.open(io.BytesIO(image_byte), formats=['PNG'])
    image.show()


if __name__ == '__main__':
    ph = photo(string="hello")
    show_image(ph)
