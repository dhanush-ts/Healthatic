from tensorflow.keras.models import load_model
import cv2
import numpy as np

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from tensorflow.keras.models import load_model


# Load the saved model
model = load_model('./skinserver/api/skin.h5')

# Preprocess the image for prediction
def preprocess_image(img_path):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (150, 150))  # Resize the image to match the input size of the model
    img = img.astype('float32') / 255.0  # Normalize pixel values to [0, 1]
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

# Function to predict the disease from an image
def predict_disease(img_path):
    processed_img = preprocess_image(img_path)
    predictions = model.predict(processed_img)
    predicted_class = np.argmax(predictions, axis=1)
    return predicted_class

# Example usage:
prediction = predict_disease('eye.jpg')
print(f"Predicted class: {prediction}")