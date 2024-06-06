import os
import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm

def preprocess_images(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for image_name in tqdm(os.listdir(input_dir)):
        img_path = os.path.join(input_dir, image_name)
        img = cv2.imread(img_path)
        img = cv2.resize(img, (640, 640))
        cv2.imwrite(os.path.join(output_dir, image_name), img)

if __name__ == "__main__":
    preprocess_images("data/images/raw", "data/images/processed")
