from PIL import Image, ImageDraw, ImageFont
import face_recognition
import os

input_img = 'target.jpeg'
output_img = 'output.jpg'

basedir = os.path.abspath(os.path.dirname(__file__))

face_list, name_list = [], []

for i in os.listdir('./images'):
    if '.DS_Store' not in i:
        image = face_recognition.load_image_file(f'{basedir}/images/{i}')
        image_encoding = face_recognition.face_encodings(image)[0]
        face_list.append(image_encoding)
        name_list.append(os.path.splitext(i)[0])

target_img = face_recognition.load_image_file(f'{basedir}/{input_img}')
face_locations = face_recognition.face_locations(target_img)
face_encodings = face_recognition.face_encodings(target_img, face_locations)

pil_img = Image.fromarray(target_img)
draw = ImageDraw.Draw(pil_img)

bk_green = (2, 215, 103)
font = ImageFont.truetype(f'{basedir}/fonts/Verdana.ttf', 28)

tolerate = 0.5

for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    matches = face_recognition.compare_faces(
        face_list, face_encoding, tolerate)
    name = 'unrecognized'

    if True in matches:
        match_index = matches.index(True)
        name = f'{name_list[match_index]}'

    draw.rectangle(((0, 0), (250, 50)), fill=bk_green, outline=bk_green)
    draw.text((10, 10), f'tolerate = {tolerate}', fill=(0, 0, 0), font=font)

    draw.rectangle(((left, top), (right, bottom)),
                   outline=bk_green, width=5)
    bbox = draw.textbbox((0, 0), text=name)
    txt_width = bbox[2] - bbox[0]
    txt_height = bbox[3] - bbox[1]

    if (right - left) / 2 < txt_width + 5:
        draw.rectangle(((left, bottom - txt_height), (right + txt_width / 1.5,
                                                      bottom + txt_height + 15)), fill=bk_green, outline=bk_green)
    else:
        draw.rectangle(((left, bottom - txt_height), (right, bottom +
                                                      txt_height + 15)), fill=bk_green, outline=bk_green)

    draw.text((left + 5, bottom - txt_height),
              name, fill=(0, 0, 0), font=font)

del draw

pil_img.save(f'{basedir}/{output_img}')

print('Completed!')
