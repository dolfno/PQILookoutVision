"""methods to manipulate the image"""

import json
from datetime import datetime

import cv2
import numpy as np
from PIL import Image


def add_text_overlay(img, text: str):
    """If anomaly show text in red otherwise in green"""
    if text == "Anomaly":
        color = (0, 0, 255)
    else:
        color = (0, 255, 0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    img_overlay = cv2.putText(img, text, (10, 30), font, 1, color, 2, cv2.LINE_AA)
    return img_overlay


def array_to_image(img) -> Image:
    return Image.fromarray(np.uint8(img))


def store_image_metadata(image_name, response):
    with open(f"{image_name}.json", "w") as outfile:
        json.dump(response, outfile)


def store_image(image, response):
    image.save(f"{datetime.now()}.png")
    store_image_metadata(image, response)
