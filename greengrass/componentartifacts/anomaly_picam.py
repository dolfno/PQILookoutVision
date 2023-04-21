import cv2
from src.edge_picamera import get_picam2
from src.edge_inference import check_for_anomalies, start_model
from src.logger import log
from src.process_image import add_text_overlay, array_to_image
import time
import grpc
from src.edge_agent_pb2_grpc import EdgeAgentStub

MODEL_COMPONENT = "binaryclassificationmodelcomponent"

if __name__ == "__main__":
    picam = get_picam2()
    # start model
    start_model(model_component=MODEL_COMPONENT)
    
    while True:
        with grpc.insecure_channel("unix:///tmp/aws.iot.lookoutvision.EdgeAgent.sock") as channel:
            stub = EdgeAgentStub(channel)
            # every 1 second, make picture and put in model and show
            # print('place next bottle')
            img = picam.capture_array()
            
            response = check_for_anomalies(img,stub, MODEL_COMPONENT)
            log.debug(f"Response: {response}")
            frame_with_text = add_text_overlay(img, response)
            cv2.imshow("frame", frame_with_text)
            time.sleep(1)
