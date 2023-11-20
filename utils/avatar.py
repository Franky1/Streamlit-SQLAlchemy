from io import BytesIO

import pyavagen
from PIL import Image, ImageDraw, ImageOps


def make_circular_thumnail(image_obj):
    """make circular thumnail from pillow image object"""
    mask = Image.new('L', image_obj.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + image_obj.size, fill=255)
    output = ImageOps.fit(image_obj, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    return output


def generate_thumbnail(string, size=64):
    '''generate avatar image as pillow image object'''
    ava = pyavagen.Avatar(pyavagen.CHAR_SQUARE_AVATAR, size=size, string=string)
    return ava.generate()


def show_image(image_obj):
    """show pillow image object"""
    image_obj.show()


def to_bytes(image_obj):
    """convert pillow image object to png file as bytes"""
    bytesio_obj = BytesIO()
    image_obj.save(bytesio_obj, format='PNG')
    return bytesio_obj.getvalue()


def generate_circular_thumbnail_bytes(string, size=64):
    """generate circular avatar image as bytesio bytes"""
    return to_bytes(make_circular_thumnail(generate_thumbnail(string=string, size=size)))


if __name__ == '__main__':
    ph = make_circular_thumnail(generate_thumbnail(string="Test"))
    show_image(ph)
