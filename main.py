from flask import Flask, render_template, url_for, request
import numpy as np
from PIL import Image
from collections import Counter

app = Flask(__name__)


def palette(arr):
    palette, index = np.unique(asvoid(arr).ravel(), return_inverse=True)
    palette = palette.view(arr.dtype).reshape(-1, arr.shape[-1])
    count = np.bincount(index)
    order = np.argsort(count)
    return palette[order[::1]]

def asvoid(arr):
    arr = np.ascontiguousarray(arr)
    return arr.view(np.dtype((np.void, arr.dtype.itemsize * arr.shape[-1])))


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':

        file = request.files['file']
        image = Image.open(file)
        resized_image = image.resize((150,150))
        data = np.array(resized_image)

        new_arr = palette(data)
        list_of_lists = new_arr.tolist()
        tuples = [tuple(x) for x in list_of_lists]

        dominant_color = Counter(tuples).most_common()[1][0]
        rgb_to_hex = '#%02x%02x%02x' % dominant_color

        return render_template('index.html', clr=dominant_color, hexclr=rgb_to_hex)

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)

