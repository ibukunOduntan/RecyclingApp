import torch
from PIL import Image
import numpy as np
import cv2
import os

def load_model(model_path, yolov5_path):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model path does not exist: {model_path}")
    model = torch.hub.load(yolov5_path, 'custom', path=model_path, source='local', force_reload=True)
    model.eval()
    return model

def get_prediction(model, image):
    results = model(image)
    return results

def draw_boxes(image, results):
    img = np.array(image)
    for *box, conf, cls in results.xyxy[0].tolist():
        label = results.names[int(cls)]
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
    return img

waste_info = {
    'Plastic': 'Plastic can be recycled by rinsing and placing in a blue recycling bin.',
    'Paper': 'Paper can be recycled by folding and placing in a green recycling bin.',
    'Glass': 'Glass should be rinsed and placed in a designated glass recycling bin.',
    'Metal': 'Metal can be recycled by rinsing and placing in a metal recycling bin.',
    'Organic': 'Organic waste can be composted or placed in a brown bin for organic waste.',
    'Electronic': 'Electronic waste should be taken to a designated e-waste recycling center.',
}
