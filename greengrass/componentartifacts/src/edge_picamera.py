"""handle the pi camera interface on the pi"""
import numpy as np
from picamera2 import Picamera2


def get_picam2() -> Picamera2:
    picam = Picamera2()
    camera_config = picam.create_preview_configuration()
    picam.configure(camera_config)
    picam.start(show_preview=True)
    return picam
