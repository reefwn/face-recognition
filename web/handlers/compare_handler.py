import face_recognition
import os

from config import Config
from PIL import Image
from utils import base64


def handle_compare(img1, img2):
    load_img1 = face_recognition.load_image_file(img1)
    load_img2 = face_recognition.load_image_file(img2)

    face_location_img1 = face_recognition.face_locations(load_img1)
    face_location_img2 = face_recognition.face_locations(load_img2)

    top, right, bottom, left = face_location_img1[0]
    coordinate_img1 = load_img1[top:bottom, left:right]
    top, right, bottom, left = face_location_img2[0]
    coordinate_img2 = load_img2[top:bottom, left:right]

    pil_img1 = Image.fromarray(coordinate_img1)
    pil_img2 = Image.fromarray(coordinate_img2)

    cropped_img1 = os.path.join(Config.CROPPED_FACE_FOLDER, 'img1.jpg')
    cropped_img2 = os.path.join(Config.CROPPED_FACE_FOLDER, 'img2.jpg')

    pil_img1.save(cropped_img1)
    pil_img2.save(cropped_img2)

    load_crop_img1 = face_recognition.load_image_file(cropped_img1)
    load_crop_img2 = face_recognition.load_image_file(cropped_img2)

    encoded_img1 = face_recognition.face_encodings(load_crop_img1)
    encoded_img2 = face_recognition.face_encodings(load_crop_img2)

    img1_base64 = base64.convert_img_to_base64(cropped_img1)
    img2_base64 = base64.convert_img_to_base64(cropped_img2)

    distance_score = face_recognition.face_distance(
        [encoded_img1[0]], encoded_img2[0])[0]
    matching = (1 - distance_score) * 100
    is_same_person = distance_score < Config.TOLERATE

    return {
        'image1': base64.add_base64_img_prefix(img1_base64),
        'image2': base64.add_base64_img_prefix(img2_base64),
        'matching': f'{matching:.2f}%',
        'is_same_person': is_same_person
    }
