"""To start the inference of the PQI demo"""
import time

import cv2
from src.process_image import add_text_overlay
from src.cloud_inference import LookoutClient
from src.laptop_webcam import get_image, save_image
from src.logger import log

if __name__ == "__main__":
    client = LookoutClient()
    status = client.get_model_status()

    if status != "HOSTED":
        client.start_model()

    while status == "STARTING_HOSTING":
        time.sleep(5)
        log.info("Waiting for model to start")
        status = client.get_model_status()

    while True:
        img_path, frame = save_image()
        response = client.detect_anomalies(img_path)
        log.debug(f"Response: {response}")
        frame_with_text = add_text_overlay(frame, "some random text")
        cv2.imshow("frame", frame_with_text)
        if cv2.waitKey(1) & 0xFF == ord("q"):  # Waits for keypress with delay of 1ms
            break
    cv2.destroyAllWindows()
