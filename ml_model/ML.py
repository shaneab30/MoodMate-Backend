import os
import argparse
from PIL import Image
from pickle import load
import numpy as np

def predict_image(image_path)->str:

    image = Image.open(image_path).convert('L')

    # (width, height) = image.size
    # # Calculate the minimum dimension to ensure a 1:1 aspect ratio
    # min_dim = min(width, height)
    # # Calculate the left and top coordinates to center the crop
    # left = (width - min_dim) // 2
    # top = (height - min_dim) // 2
    # # Crop the image to a 1:1 aspect ratio
    # image = image.crop((left, top, left + min_dim, top + min_dim))
    image = image.resize((48, 48))
    image = np.array(image).flatten()
    image = image/255.0

    image = image.reshape(1, -1)  
    # image.save(f'resized_{image_name}.png')
    print(image)

    # scale image with standard scaler
    X_scaled, y_encoded,label_encoder, pca, scaler = load(open("ml_model/labelencoder_standardscaler_pca_normalizers_dump.pkl", "rb"))
    image = pca.transform(image)
    image = scaler.transform(image)

    # machine learning
    svc_model = load(open("ml_model/knn_model_standardscaler_grisearch_pca_dump.pkl", "rb"))
    y = svc_model.predict(image)

    label = label_encoder.inverse_transform(y)
    # label = label_encoder.inverse_transform([y])

    print(label)
    return label.tolist()[0]