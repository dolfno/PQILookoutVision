import json
import time as t

import src.edge_agent_pb2 as pb2
from src.edge_agent_pb2_grpc import EdgeAgentStub
import grpc
import numpy as np
from awscrt import io, mqtt
from awsiot import mqtt_connection_builder

from picamera2 import Picamera2
from PIL import Image
import time
import datetime
import pathlib
import argparse
import sys
import os
		
ENDPOINT = "a1t2xj7x9iehh6-ats.iot.eu-west-1.amazonaws.com"
CLIENT_ID = "PQICore"
PATH_TO_CERTIFICATE = "/greengrass/v2/thingCert.crt"
PATH_TO_PRIVATE_KEY = "/greengrass/v2/privKey.key"
PATH_TO_AMAZON_ROOT_CA_1 = "/greengrass/v2/rootCA.pem"
TOPIC = "l4v/testclient"
MODEL_COMPONENT = "tobe"

CURRENT_PATH = pathlib.Path(__file__).parent.resolve()

def start_model_if_needed(stub, model_name):
    # Starting model if needed.
    while True:
        model_description_response = stub.DescribeModel(pb2.DescribeModelRequest(model_component=model_name))
        if model_description_response.model_description.status == pb2.RUNNING:
            print("Model is already running.")
            break
        elif model_description_response.model_description.status == pb2.STOPPED:
            print("Starting the model.")
            stub.StartModel(pb2.StartModelRequest(model_component=model_name))
            continue
        print(f"Waiting for model to start.")
        if model_description_response.model_description.status != pb2.STARTING:
            break
        time.sleep(1.0)
        
def detect_anomalies(img, channel):
    stub = EdgeAgentStub(channel)
    start_model_if_needed(stub, MODEL_COMPONENT)
    h, w, c = img.shape
    print("shape=" + str(img.shape))
    response = stub.DetectAnomalies(
        pb2.DetectAnomaliesRequest(
            model_component=MODEL_COMPONENT, bitmap=pb2.Bitmap(width=w, height=h, byte_data=bytes(img.tobytes()))
        )
    )
    print("is_anomalous:" + str(response.detect_anomaly_result.is_anomalous))
    print(str(response))
    return response

def connect_mqtt():
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=ENDPOINT,
        cert_filepath=PATH_TO_CERTIFICATE,
        pri_key_filepath=PATH_TO_PRIVATE_KEY,
        client_bootstrap=client_bootstrap,
        ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
        client_id=CLIENT_ID,
        clean_session=False,
        keep_alive_secs=6,
    )
    print("Connecting to {} with client ID '{}'...".format(ENDPOINT, CLIENT_ID))
    # Make the connect() call
    connect_future = mqtt_connection.connect()
    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")
    return mqtt_connection
    


def publish_mqtt_message(mqtt_connection, response):
    # Publish message to server desired number of times.
    print("Begin Publish")
    data = "{} [{}]".format(str(response), 1)
    message = {"message": data, "is_anomalous": response.detect_anomaly_result.is_anomalous}
    mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
    print("Published: '" + json.dumps(message) + "' to the topic: " + TOPIC)
    t.sleep(0.1)
    print("Publish End")


def disconnect_mqtt(mqtt_connection):
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()

class ANOMA:
	is_anomalous = 1
	
class TEST_RESPONSE:
	detect_anomaly_result = ANOMA

def start_camera():
	picam2 = Picamera2()
	camera_config = picam2.create_preview_configuration()
	camera_config['main']['size'] = (1080, 720)
	picam2.configure(camera_config)
	picam2.start(show_preview=True)
	return picam2

def store_image(picam2, anomaly=False):
	im = picam2.capture_array()		
	img = Image.fromarray(im)
	image_name = f"{datetime.datetime.now()}.png"
	anomaly_folder = "anomaly" if anomaly else "normal"
	path_to_folder = f'Images/{anomaly_folder}'
	if not os.path.exists(path_to_folder):
	    os.makedirs(path_to_folder)
	img.save(f"{CURRENT_PATH}/{path_to_folder}/{image_name}")
	print(f"Stored {anomaly_folder} images {image_name}")

def argparser():
    parser = argparse.ArgumentParser(description='anomaly or normal')
    parser.add_argument("bottletype", type=str)
    args = parser.parse_args()
    bottletype = args.bottletype
    return bottletype

def main():
    bottletype = argparser()
    picam2 = start_camera()


    while True:

        if bottletype == "anomaly":
            store_image(picam2, anomaly=True)
            time.sleep(3)	    
        if bottletype == "normal":
            store_image(picam2, anomaly=False)
            time.sleep(3)

	
		
    """
	# Creating stub.
	with grpc.insecure_channel("unix:///tmp/aws.iot.lookoutvision.EdgeAgent.sock") as channel:
		stub = EdgeAgentStub(channel)
		
		models_list_response = stub.ListModels(
			pb2.ListModelsRequest()
		)
		print(f"found {models_list_response}")
		for model in models_list_response.models:
			print(f"Model Details {model}")
    """

		# mqtt_connection = connect_mqtt()
		# response = detect_anomalies(im, channel)
		# publish_mqtt_message(mqtt_connection, TEST_RESPONSE)
		# disconnect_mqtt(mqtt_connection)
		# img.show()


    # # After the loop release the cap object
    # vid.release()
    # # Destroy all the windows
    # cv2.destroyAllWindows()




#     picam2 = Picamera2()
#     camera_config = picam2.create_preview_configuration()
#     picam2.configure(camera_config)
#     picam2.start()
#     im = picam2.capture_array()
#     img = Image.fromarray(np.uint8(im))
#     img.show()

if __name__ == "__main__":
	main()
