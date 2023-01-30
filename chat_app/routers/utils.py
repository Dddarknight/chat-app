import io
from PIL import Image


def get_image_value(image_file_content, size):
    image_pil = Image.open(io.BytesIO(image_file_content)).resize(size)
    buffer = io.BytesIO()
    image_pil.save(buffer, format="JPEG")
    return buffer.getvalue()
