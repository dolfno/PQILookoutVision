import src.edge_agent_pb2 as pb2
import grpc
from src.edge_agent_pb2_grpc import EdgeAgentStub
from src.logger import log
import cv2
import time

def start_model(model_component):
    with grpc.insecure_channel("unix:///tmp/aws.iot.lookoutvision.EdgeAgent.sock") as channel:
        log.debug("channel set")
        stub = EdgeAgentStub(channel)
        status_code = stub.DescribeModel(pb2.StartModelRequest(model_component=model_component)).model_description.status
        
        if status_code != 2:
            print("start model")
            stub.StartModel(pb2.StartModelRequest(model_component=model_component))
        while status_code != 2:
            print(f"model is starting, with status code {status_code}")
            time.sleep(3)
            status_code = stub.DescribeModel(pb2.StartModelRequest(model_component=model_component)).model_description.status
        return True

def check_for_anomalies(img, stub, model_component):
    image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, c = img.shape
    log.debug("shape=" + str(image_rgb.shape))
    detect_anomalies_response = stub.DetectAnomalies(
        pb2.DetectAnomaliesRequest(
            model_component=model_component,
            bitmap=pb2.Bitmap(width=w, height=h, byte_data=bytes(image_rgb.tobytes())),
        )
    )
    return detect_anomalies_response

