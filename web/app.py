import os

from config import Config
from flask import Flask, render_template, flash
from flask_cors import CORS
from forms import CompareForm
from handlers.compare_handler import handle_compare
from utils import image


app = Flask(__name__)
CORS(app)

app.config.from_object(Config)

os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(Config.CROPPED_FACE_FOLDER, exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/compare', methods=['GET', 'POST'])
def compare():
    form = CompareForm()
    if form.validate_on_submit():
        file_path1 = image.upload_image(form.image1)
        file_path2 = image.upload_image(form.image2)

        data = handle_compare(file_path1, file_path2)

        flash('Images successfully uploaded', 'success')

        return render_template('compare-result.html', **data)

    return render_template('compare.html', form=form)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
