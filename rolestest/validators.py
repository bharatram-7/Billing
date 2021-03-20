from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.core.files.images import get_image_dimensions


def image_restriction(image):
    image_width, image_height = get_image_dimensions(image)
    if image_width > 900 or image_height > 900:
        raise ValidationError("Image width/height needs to be less than or equal to 900px")
    if not image_width == image_height:
        raise ValidationError("Image width needs to be equal to it's height")

