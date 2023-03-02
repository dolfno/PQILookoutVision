import edge_agent_pb2 as pb2
import grpc
from edge_agent_pb2_grpc import EdgeAgentStub
from src.logger import log


def check_for_anomalies(img, model_component):
    with grpc.insecure_channel("unix:///tmp/aws.iot.lookoutvision.EdgeAgent.sock") as channel:
        log.debug("channel set")
        stub = EdgeAgentStub(channel)
        h, w, c = img.shape
        log.debug("shape=" + str(img.shape))
        detect_anomalies_response = stub.DetectAnomalies(
            pb2.DetectAnomaliesRequest(
                model_component=model_component,
                bitmap=pb2.Bitmap(width=w, height=h, byte_data=bytes(img.tobytes())),
            )
        )
        return detect_anomalies_response
