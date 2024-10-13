import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os

# Disable OneDNN optimizations for TensorFlow if necessary
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Load your pre-trained model (updated version)
model = load_model('./skinserver/api/skin.h5')

# Updated list of 13 skin disease classes
disease_labels = ['Eczema', 'Warts', 'Melanoma', 'Atopic', 'Basal', 'Melanocytic',
                  'Benign', 'Psoriasis', 'Seborrheic', 'Tinea', 'Acne', 'Vitiligo', 'Chickenpox']

# Function to preprocess the input image for prediction
def preprocess_image(image):
    image = cv2.resize(image, (150, 150))  # Resize the image to match the model input
    image = image.astype('float32') / 255.0  # Normalize pixel values to [0, 1]
    image = np.expand_dims(image, axis=0)  # Add batch dimension (1, 150, 150, 3)
    return image

# Function to predict the top 4 skin diseases from the image
def predict_top_4_diseases(image, model, disease_labels):
    try:
        processed_img = preprocess_image(image)

        # Get predictions from the model
        predictions = model.predict(processed_img)

        # Get the top 4 diseases with the highest probabilities
        top_4_indices = np.argsort(predictions[0])[-4:][::-1]  # Get indices of top 4 predictions
        top_4_diseases = [disease_labels[i] for i in top_4_indices]
        return top_4_diseases
    except Exception as e:
        print(f"Error during prediction: {e}")
        return []

# Function to select and upload an image for prediction
def upload_and_predict():
    # Open file dialog to select an image file
    Tk().withdraw()  # Hide the root Tkinter window
    image_path = askopenfilename(title="Select an Image", filetypes=[("Image files", "*.jpg *.jpeg *.png")])

    if not image_path:
        print("No image selected.")
        return

    # Read the uploaded image
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Unable to read the image at {image_path}")
        return

    # Predict the top 4 diseases from the image
    top_4_diseases = predict_top_4_diseases(image, model, disease_labels)

    if top_4_diseases:
        print(f"Top 4 predicted diseases: {', '.join(top_4_diseases)}")
    else:
        print("Prediction error")

# Run the image upload and prediction function
upload_and_predict()
