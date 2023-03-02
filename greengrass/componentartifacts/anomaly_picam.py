import cv2
from src.edge_inference import check_for_anomalies
from src.edge_picamera import get_picam2
from src.logger import log
from src.process_image import add_text_overlay, array_to_image

MODEL_COMPONENT = "binaryclassificationmodelcomponent"

if __name__ == "__main__":
    picam = get_picam2()
    while True:
        img = picam.capture_array()
        response = check_for_anomalies(img, MODEL_COMPONENT)
        log.debug(f"Response: {response}")
        frame_with_text = add_text_overlay(array_to_image(img), response)
        cv2.imshow("frame", frame_with_text)
        if cv2.waitKey(1) & 0xFF == ord("q"):  # Waits for keypress with delay of 1ms
            break
