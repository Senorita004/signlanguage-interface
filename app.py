from flask import Flask, request, jsonify, send_from_directory
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
import numpy as np
import io

app = Flask(__name__, static_folder='public')

# Constants
SEQUENCE_LENGTH = 10

labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# Load your models
model_cnn = load_model("./models/model_cnn.h5")
model_lstm = load_model("./models/model_lstm.h5")
model_multi_lstm = load_model("./models/model_multi_lstm.h5")
model_rnn = load_model("./models/model_rnn.h5")

def resize_image(img, target_size):
    """Resize and normalize the image for CNN."""
    if img.mode != "RGB":
        img = img.convert("RGB")
    img = img.resize(target_size)
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def preprocess_for_rnn(img, sequence_length, target_size):
    """Preprocess the image for RNN."""
    if img.mode != "RGB":
        img = img.convert("RGB")
    img = img.resize(target_size)
    img_array = image.img_to_array(img) / 255.0

    # Create a dummy sequence
    sequence = np.tile(img_array, (sequence_length, 1, 1, 1))
    sequence = sequence.reshape(1, sequence_length, *target_size, 3)
    return sequence

def preprocess_for_lstm(img, sequence_length, target_size):
    """Preprocess the image for LSTM."""
    if img.mode != "RGB":
        img = img.convert("RGB")
    img = img.resize(target_size)
    img_array = image.img_to_array(img) / 255.0

    flattened_img = img_array.reshape(-1) 

    sequence = np.tile(flattened_img, (sequence_length, 1))

    sequence = sequence.reshape(1, sequence_length, -1)

    return sequence

def preprocess_for_multi_lstm(img, sequence_length, target_size):
    """Preprocess the image for multi-layer LSTM."""
    if img.mode != "RGB":
        img = img.convert("RGB")
    img = img.resize(target_size)
    img_array = image.img_to_array(img) / 255.0 

    flattened_img = img_array.reshape(-1)

    sequence = np.tile(flattened_img, (sequence_length, 1))

    sequence = sequence.reshape(1, sequence_length, -1) 

    return sequence

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files["file"]
    model_name = request.form.get("model", "cnn")

    print("model_name")
    print(model_name)

    if file.filename == "":
        return jsonify({"error": "No selected file"})

    image = Image.open(io.BytesIO(file.read()))
    
    if model_name == "cnn":
        resized_image = resize_image(image, target_size=(64, 64))
        prediction = model_cnn.predict(resized_image)
    elif model_name == "rnn":
        processed_image = preprocess_for_rnn(image, SEQUENCE_LENGTH, target_size=(64, 64))
        prediction = model_rnn.predict(processed_image)
    elif model_name == "lstm":
        processed_image = preprocess_for_lstm(image, SEQUENCE_LENGTH, target_size=(64, 64))
        prediction = model_lstm.predict(processed_image)
    elif model_name == "multi_lstm":
        processed_image = preprocess_for_multi_lstm(image, SEQUENCE_LENGTH, target_size=(64, 64))
        prediction = model_multi_lstm.predict(processed_image)
    else:
        return jsonify({"error": "Invalid model name"})

    predicted_class = np.argmax(prediction)
    response = {
        "predicted_class": int(predicted_class),
        "predicted_value": labels[int(predicted_class)],
        "confidence": float(np.max(prediction)),
    }

    return jsonify(response)


@app.route('/')
def home():
    return send_from_directory('public', 'index.html')

# Serve static files
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('public', path)

if __name__ == "__main__":
    app.run(port=8000, debug=True)
