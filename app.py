from flask import Flask, render_template, request, redirect, url_for
import torch
from PIL import Image
import numpy as np
import cv2
import os
from app_utils import load_model, get_prediction, draw_boxes, waste_info
import base64
from io import BytesIO

app = Flask(__name__)

# Model path
model_path = os.path.join('model', 'best.pt')
yolov5_path = 'yolov5'

# Load the model
model = load_model(model_path, yolov5_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    if file:
        image = Image.open(file.stream).convert('RGBA')  # Ensure the image is in RGBA mode
        results = get_prediction(model, image)
        img_with_boxes = draw_boxes(image, results)
        
        # Convert numpy array to PIL Image
        img_with_boxes = Image.fromarray(img_with_boxes)

        # Remove alpha channel if present
        if img_with_boxes.mode == 'RGBA':
            img_with_boxes = img_with_boxes.convert('RGB')

        # Convert image with boxes to base64 string
        buffered = BytesIO()
        img_with_boxes.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        labels = results.pandas().xyxy[0]['name'].unique().tolist()
        return render_template('result.html', labels=labels, img_data=img_str)

@app.route('/recycle/<material>')
def recycle(material):
    return render_template(f'{material.lower()}.html')


@app.route('/about')
def about():
    return render_template('about.html')
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8000)
