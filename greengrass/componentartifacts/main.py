"""To start the inference of the PQI demo"""
import time

import cv2 #TODO replace with picamera and make cv2 obsolute, cause massive overhead on pi;
from src.cloud_inference import LookoutClient
from src.laptop_webcam import get_image, save_image
from src.logger import log
from src.process_image import add_text_overlay

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
        frame = add_text_overlay(frame, response)
        cv2.imshow("frame", frame) # TODO replace with picamera

        log.info(f"Response: {response}")
        if cv2.waitKey(1) & 0xFF == ord("q"):  # Waits for keypress with delay of 1ms
            break
    cv2.destroyAllWindows()
"""
 # {'ResponseMetadata': {'RequestId': '495a1a06-fc9d-4673-a0b9-58910fc220a9', 'HTTPStatusCode': 200, 
 'HTTPHeaders': {'x-amzn-requestid': '495a1a06-fc9d-4673-a0b9-58910fc220a9', 'x-xss-protection':
  '1; mode=block', 'strict-transport-security': 'max-age=31540000; includeSubDomains', 
  'x-frame-options': 'DENY', 'x-content-type-options': 'nosniff', 'date': 'Thu, 02 Mar 2023 13:03:56 GMT', 
  'content-type': 'application/json', 'content-length': '103'}, 'RetryAttempts': 0}, 
  'DetectAnomalyResult': {'Source': {'Type': 'direct'}, 'IsAnomalous': True, 'Confidence': 0.9979099631309509}}
"""