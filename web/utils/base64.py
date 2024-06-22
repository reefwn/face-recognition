import base64


def convert_img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read())
    return encoded_string.decode('utf-8')


def convert_base64_to_img(img_base64, img_path, extension):
    with open(f'{img_path}.{extension}', 'wb') as f:
        f.write(base64.decodebytes(str.encode(img_base64)))


def add_base64_img_prefix(base64_string):
    return f'data:image/jpeg;base64,{base64_string}'
