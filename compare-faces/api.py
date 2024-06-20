from flask import Flask, request, jsonify
from flask_cors import CORS
import face_recognition
from PIL import Image
import base64
import os

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
img_path = basedir + '/images'
img_path_original = img_path + '/original/'
img_path_idcard = img_path + '/idcard/'
img_path_selfie = img_path + '/selfie/'


@app.route('/', methods=['GET'])
def home():
    return 'image processing service'


def convert_img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read())
    return encoded_string


def convert_base64_to_img(img_base64, img_path, extension):
    with open(f'{img_path}.{extension}', 'wb') as f:
        f.write(base64.decodebytes(str.encode(img_base64)))


@app.route('/compare-images', methods=['POST'])
def image_processing():

    if not request.json['img1_base64'] or not request.json['img2_base64']:
        return jsonify(status="error", message="PLEASE_UPLOAD_2_IMAGES_TO_CONTINUE")

    img1_base64 = request.json['img1_base64']
    img2_base64 = request.json['img2_base64']
    img_extension = request.json['img_extension']
    customer_name = request.json['customer_name']
    tolerate = request.json['tolerate']

    convert_base64_to_img(
        img1_base64, f'{img_path_original}{customer_name}-1', img_extension)
    convert_base64_to_img(
        img2_base64, f'{img_path_original}{customer_name}-2', img_extension)

    load_img1 = face_recognition.load_image_file(
        f'{img_path_original}{customer_name}-1.{img_extension}')
    load_img2 = face_recognition.load_image_file(
        f'{img_path_original}{customer_name}-2.{img_extension}')

    facelocation_img1 = face_recognition.face_locations(load_img1)
    facelocation_img2 = face_recognition.face_locations(load_img2)

    if len(facelocation_img1) > 1 or len(facelocation_img2) > 1:
        return jsonify(status="error", message="DETECT_MORE_THAN_ONE_FACE_IN_A_PICTURE")

    if len(facelocation_img1) < 1 or len(facelocation_img2) < 1:
        return jsonify(status="error", message="NO_FACE_DETECTED")

    top, right, bottom, left = facelocation_img1[0]
    coordinate_img1 = load_img1[top:bottom, left:right]
    top, right, bottom, left = facelocation_img2[0]
    coordinate_img2 = load_img2[top:bottom, left:right]

    pil_img1 = Image.fromarray(coordinate_img1)
    pil_img2 = Image.fromarray(coordinate_img2)

    pil_img1.save(f'{img_path_idcard}{customer_name}-1.{img_extension}')
    pil_img2.save(f'{img_path_selfie}{customer_name}-2.{img_extension}')

    loadcrop_img1 = face_recognition.load_image_file(
        f'{img_path_idcard}{customer_name}-1.{img_extension}')
    loadcrop_img2 = face_recognition.load_image_file(
        f'{img_path_selfie}{customer_name}-2.{img_extension}')

    encoded_img1 = face_recognition.face_encodings(loadcrop_img1)
    encoded_img2 = face_recognition.face_encodings(loadcrop_img2)

    if not encoded_img1 or not encoded_img2:
        return jsonify(status="error", message="CANNOT_ENCODE_IMAGE")

    idcard_img = convert_img_to_base64(
        f'{img_path_idcard}{customer_name}-1.{img_extension}')
    selfie_img = convert_img_to_base64(
        f'{img_path_selfie}{customer_name}-2.{img_extension}')

    ds = face_recognition.face_distance([encoded_img1[0]], encoded_img2[0])[0]
    isp = ds < tolerate

    return jsonify(status="success", idcard_img=idcard_img.decode('utf-8'), selfie_img=selfie_img.decode('utf-8'), is_same_person=str(isp).lower(), diff_score=ds)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
