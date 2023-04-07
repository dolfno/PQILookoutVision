
import grpc
import src.edge_agent_pb2 as pb2 
from src.edge_agent_pb2_grpc import (
            EdgeAgentStub
)
def warm_up(model_component):
	channel = grpc.insecure_channel("unix:///tmp/aws.iot.lookoutvision.EdgeAgent.sock")
	stub = EdgeAgentStub(channel)
	stub.StartModel(pb2.StartModelRequest(model_component=model_component))
	
