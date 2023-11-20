from io import BytesIO
import random

import py_avataaars as pa
from PIL import Image, ImageDraw, ImageOps


def resize_square_image(image_obj, size):
    '''resize image to square image'''
    return image_obj.resize((size, size))


def make_circular_thumnail(image_obj):
    """make circular thumnail from pillow image object"""
    mask = Image.new('L', image_obj.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + image_obj.size, fill=255)
    output = ImageOps.fit(image_obj, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    return output


def generate_thumbnail():
    '''generate avatar image as pillow image object'''
    avatar = pa.PyAvataaar(
        style=random.choice(list(pa.AvatarStyle)),
        skin_color=random.choice(list(pa.SkinColor)),
        hair_color=random.choice(list(pa.HairColor)),
        facial_hair_type=random.choice(list(pa.FacialHairType)),
        facial_hair_color=random.choice(list(pa.HairColor)),
        top_type=random.choice(list(pa.TopType)),
        hat_color=random.choice(list(pa.Color)),
        mouth_type=random.choice(list(pa.MouthType)),
        eye_type=random.choice(list(pa.EyesType)),
        eyebrow_type=random.choice(list(pa.EyebrowType)),
        nose_type=random.choice(list(pa.NoseType)),
        accessories_type=random.choice(list(pa.AccessoriesType)),
        clothe_type=random.choice(list(pa.ClotheType)),
        clothe_color=random.choice(list(pa.Color)),
        clothe_graphic_type=random.choice(list(pa.ClotheGraphicType)),
    )
    png_bytes = avatar.render_png()
    return Image.open(BytesIO(png_bytes), formats=['PNG'])


def show_image(image_obj):
    """show pillow image object"""
    image_obj.show()


def to_bytes(image_obj):
    """convert pillow image object to png file as bytes"""
    bytesio_obj = BytesIO()
    image_obj.save(bytesio_obj, format='PNG')
    return bytesio_obj.getvalue()


def generate_circular_thumbnail_bytes(size=128):
    """generate circular avatar image as bytesio bytes"""
    return to_bytes(make_circular_thumnail(resize_square_image(generate_thumbnail(), size=size)))


if __name__ == '__main__':
    ph = make_circular_thumnail(resize_square_image(generate_thumbnail(), size=128))
    show_image(ph)
