"""handle webcam interface for laptop"""
"""interact with the local macbook camera"""

import os
from typing import Tuple
import cv2
from PIL import Image
from datetime import datetime
import numpy as np


def get_image():
    """get image from webcam"""
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    return frame


def save_image(img_path: str = None, resolution: tuple = (1080, 720)) -> Tuple[str, np.array]:
    """taking a picture and saving it a img_path

    Args:
        img_path (str, optional): Defaults to None.

    Returns:
        Tuple[str, np.array]: path to image and image as numpy array
    """
    frame = get_image()
    im = Image.fromarray(frame).resize(resolution)
    img_folder = "raw_images"
    # if img folder is not there, create it
    if not os.path.exists(img_folder):
        os.mkdir(img_folder)
    img_path = img_path if img_path else f"./{img_folder}/{datetime.now()}.png"
    im.save(img_path)
    return img_path, frame
