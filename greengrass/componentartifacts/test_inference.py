import json
import time as t

import src.edge_agent_pb2 as pb2
# import cv2
import grpc
import numpy as np
from awscrt import io, mqtt
from awsiot import mqtt_connection_builder
from src.edge_agent_pb2_grpc import EdgeAgentStub
from picamera2 import Picamera2
from PIL import Image
from src.logger import log

ENDPOINT = "a1t2xj7x9iehh6-ats.iot.eu-west-1.amazonaws.com"
CLIENT_ID = "PQICore"
PATH_TO_CERTIFICATE = "/greengrass/v2/thingCert.crt"
PATH_TO_PRIVATE_KEY = "/greengrass/v2/privKey.key"
PATH_TO_AMAZON_ROOT_CA_1 = "/greengrass/v2/rootCA.pem"
TOPIC = "l4v/testclient"
MODEL_COMPONENT = "tobe"

def detect_anomalies(img, channel):
    stub = EdgeAgentStub(channel)
    print("channel set")
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

def detect_anomalies(a, b):
    return {
        "detect_anomaly_result": {}
    }

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
    print(response)
    data = "{} [{}]".format(str(response), 1)
    message = {"message": data, "is_anomalous": response.detect_anomaly_result.is_anomalous}
    mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
    print("Published: '" + json.dumps(message) + "' to the topic: " + TOPIC)
    t.sleep(0.1)
    print("Publish End")


def disconnect_mqtt(mqtt_connection):
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()


with grpc.insecure_channel("unix:///tmp/aws.iot.lookoutvision.EdgeAgent.sock") as channel:
    picam2 = Picamera2()
    camera_config = picam2.create_preview_configuration()
    picam2.configure(camera_config)
    picam2.start()
    im = picam2.capture_array()
    img = Image.fromarray(np.uint8(im))
    img.show()

    mqtt_connection = connect_mqtt()
    response = detect_anomalies(im, channel)
    publish_mqtt_message(mqtt_connection, response)
    disconnect_mqtt(mqtt_connection)


    # # After the loop release the cap object
    # vid.release()
    # # Destroy all the windows
    # cv2.destroyAllWindows()


# def main():
    # picam2 = Picamera2()
    # camera_config = picam2.create_preview_configuration()
    # picam2.configure(camera_config)
    # picam2.start()
    # im = picam2.capture_array()
    # img = Image.fromarray(np.uint8(im))
    # img.show()

# if __name__ == "__main__":
    # main()

def store_image_metadata(image_name, response):
    with open(f"{image_name}.json", "w") as outfile:
        json.dump(response, outfile)

def store_image(image, response):
    image.save(f"{datetime.now()}.png")
    store_image_metadata(image, response)
