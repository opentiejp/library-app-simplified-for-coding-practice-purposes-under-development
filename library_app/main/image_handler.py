import os

from PIL import Image
from flask import current_app


def add_featured_image(uploaded_image):
    image_filename = uploaded_image.filename
    filepath = os.path.join(current_app.root_path, 'static/featured_image', image_filename)
    image_size = (800, 800)
    image = Image.open(uploaded_image)
    image.thumbnail(image_size)
    image.save(filepath)
    return image_filename
