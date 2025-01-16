import os
from django.core.exceptions import ValidationError
from PIL import Image
from django.utils.translation import gettext_lazy as _
import imghdr


def validate_square_image(image):
    img = Image.open(image)
    ratio = img.width / img.height
    if ratio < 0.9 or ratio > 1.1:
        # raise ValidationError(_("Invalid image. The image must be square."))
        raise ValidationError("Изображение должно быть квадратным.")

square_image_validator = {
    'help_text': 'Изображение должно быть квадратным',
    'validators': [validate_square_image, ],
}


def validate_horizontal_image(image):
    img = Image.open(image)
    if img.width <= img.height:
        # raise ValidationError(_("Invalid image. The image must be horizontal (width must be greater than height)."))
        raise ValidationError("Изображение должно быть горизонтальным (ширина должна быть больше высоты).")

horizontal_image_validator = {
    'help_text': 'Изображение должно быть горизонтальным',
    'validators': [validate_horizontal_image, ],
}


def validate_vertical_image(image):
    img = Image.open(image)
    if img.width >= img.height:
        # raise ValidationError(_("Invalid image. The image must be vertica (height must be greater than width)."))
        raise ValidationError("Изображение должно быть вертикальным (ширина должна быть больше высоты).")

vertical_image_validator = {
    'help_text': 'Изображение должно быть вертикальным',
    # 'help_text': _('The image must be vertical'),
    'validators': [validate_vertical_image, ],
}


def validate_pdf_file(file):
    # Проверяем расширение файла
    ext = os.path.splitext(file.name)[1].lower()
    if ext != '.pdf':
        raise ValidationError("Недопустимое расширение файла. Разрешены только PDF-файлы.")

    # Проверяем MIME тип файла
    # if file.content_type != 'application/pdf':
    #     raise ValidationError(_("Invalid file type. Only PDF files are allowed."))

pdf_file_validate = {
    'validators': [validate_pdf_file],
    'help_text':"Разрешены только PDF-файлы.",
}


def validate_png_image(image):
    image_format = imghdr.what(image)
    if image_format != 'png':
        raise ValidationError('Недопустимый формат изображения. Допустимый формат - "PNG"..')
        # raise ValidationError('Неверный формат изображения. Разрешенный формат "PNG".')

png_image_validator = {
    'help_text': 'Изображение должно быть в формате "PNG"',
    'validators': [validate_png_image, ],
}


correct_video_formats = ['mp4', 'webm', 'avi', 'mov']

def validate_video(video):
    video_format = imghdr.what(video)
    if video_format:
        allowed_formats = correct_video_formats
        if video_format.lower() not in allowed_formats:
            raise ValidationError(_(f'Invalid video format. Allowed format: ') + allowed_formats)
            # raise ValidationError('Неверный формат изображения. Разрешенный формат "PNG".')

video_validator = {
    'help_text': (_(f'The video in format: ') + str(correct_video_formats)),
    'validators': [validate_video, ],
}