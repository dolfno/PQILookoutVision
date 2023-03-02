# Prepare raspberry pi for edge setup to support greengrass deployment

## 1. Install Raspbian OS 64 bit with desktop
Use [raspberry pi imager](https://www.raspberrypi.com/software/) to install Raspbian OS 64 bit with desktop.
Configure:
- allow ssh
- set wifi

## 2. Install greengrass v2

1. ssh into pi
2. install java, run below and wait a while..
```
yes Y | sudo apt-get update
yes Y | sudo apt-get upgrade
yes Y | sudo apt install default-jdk
```
3. Install the AWS IoT Greengrass Core software ([based on Step 3 here](https://docs.aws.amazon.com/greengrass/v2/developerguide/getting-started.html#install-greengrass-v2))

* Install greengrass installer
```
cd ~
curl -s https://d2s8p88vqu9w66.cloudfront.net/releases/greengrass-nucleus-latest.zip > greengrass-nucleus-latest.zip
unzip greengrass-nucleus-latest.zip -d GreengrassInstaller && rm greengrass-nucleus-latest.zip
```
* install aws cli v2
```
curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```
* Authenticate aws cli, either via installing saml2aws or export your local env | grep AWS variables after ao'ing into aws account (if `aws s3 ls` works your are ready for last step.)


* For Step 3.4 `Run the following command to launch the AWS IoT Greengrass Core software installer` 
We use the below code snippet:
```
sudo -E java -Droot="/greengrass/v2" -Dlog.store=FILE \
  -jar ./GreengrassInstaller/lib/Greengrass.jar \
  --aws-region eu-west-1 \
  --thing-name PQICore \
  --thing-group-name PQICoreGroup \
  --thing-policy-name PQIIoTThingPolicy \
  --tes-role-name PQITokenExchangeRole \
  --tes-role-alias-name PQICoreTokenExchangeRoleAlias \
  --component-default-user ggc_user:ggc_group \
  --provision true \
  --setup-system-service true \
  --deploy-dev-tools true
```
Example console output:
![Example console output](./console-output.jpg)

Your raspberry pi edge is now ready to receive greengrass deployments.  
[Optional] Go to aws console -> IoT Core to see if the device is registered.

## after check that open cv is not working, go here;
https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf 