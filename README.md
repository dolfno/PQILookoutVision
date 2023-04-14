# PQILookoutVision
Demo environment for the lookout for vision demo running in robohouse

## Installation
Prepare edge device (raspberry pi 4) with greengrass core and opencv 4.5.5 see [here](./edgesetup/pi_setup.md)

## Greengrass deployment
see [./greengrass](./greengrass/deployment.md)


# TODO check this to improve
https://github.com/aws-samples/amazon-lookout-for-vision/blob/main/edge/install_greengrass.sh

iam role should have access to s3
s3:GetObject

In greengrass/component artifacts
Before running any scripts, in your terminal type:
pip install -r requirements.txt
Scripts:
To gather data:
gather_data.py: takes a picture every 3 seconds and stores it in Images/anomaly or Images/normal.
For your anomaly samples run: python gather_data.py anomaly
For normal samples: python gather_data.py normal
//Train model with your data in AWS see Confluence to know how///
To run inference:
anomaly_picam: this script runs the main function that calls to take a picture with the picam and run inference. This is the script to run for the demo
In the terminal: python anomaly_picam.py

anomaly_webcam: test script to run on your laptop. Calls to take a picture with your webam and run inference
In the terminal: python anomaly_webcam.py

