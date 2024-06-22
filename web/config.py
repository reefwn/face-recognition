import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
    CROPPED_FACE_FOLDER = os.getenv('CROPPED_FACE_FOLDER')
    TOLERATE = float(os.getenv('TOLERATE'))
