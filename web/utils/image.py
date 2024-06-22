import os

from config import Config
from werkzeug.utils import secure_filename


def upload_image(image):
    file = image.data
    filename = secure_filename(file.filename)
    file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
    file.save(file_path)

    return file_path
