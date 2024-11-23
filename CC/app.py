import numpy as np
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from PIL import Image

app = Flask(__name__)

model = load_model('../model_fruit.h5')

def process_image(image):
    image = image.convert('RGB')

    image = image.resize((224, 224))

    image_array = np.array(image) / 255.0

    image_array = np.expand_dims(image_array, axis=0)

    return image_array


@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files['input']

        image = Image.open(file.stream)
        input_data = process_image(image)

        prediction = model.predict(input_data)

        prediction = prediction.tolist()[0][0]

        deskripsi = {
            0: "Segar",
            1: "Busuk",
        }

        return jsonify({'prediction': deskripsi[round(prediction)]})
        # return jsonify({'prediction': (prediction)})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/')
@app.route('/index')
def index():
    return jsonify({'message': 'running..'})

if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=4000)
    app.run(debug=False, host='0.0.0.0', port=4000)
