"""to interact with the model in the cloud"""
"""interact with the cloud lookout for vision api"""
import boto3
from mypy_boto3_lookoutvision.client import LookoutforVisionClient
from mypy_boto3_lookoutvision.type_defs import DetectAnomaliesResponseTypeDef
from src.logger import log

boto3.setup_default_session(region_name="eu-west-1")


class LookoutClient:
    def __init__(self, project_name: str = None, model_version: int = None):
        self._client: LookoutforVisionClient = None
        self.project_name = project_name if project_name else self.get_first_project()
        self.model_version = model_version if model_version else self.get_first_model_version()

    @property
    def client(self) -> LookoutforVisionClient:
        if not self._client:
            self._client = boto3.client("lookoutvision")
        return self._client

    def detect_anomalies(self, image_path) -> DetectAnomaliesResponseTypeDef:
        """detect anomalies in image"""
        with open(image_path, "rb") as image:
            response = self.client.detect_anomalies(
                ProjectName=self.project_name,
                ModelVersion=self.model_version,
                ContentType="image/png",
                Body=image.read(),
            )
        return response

    def get_first_project(self) -> str:
        """get first project"""
        response = self.client.list_projects()
        try:
            project_name = response["Projects"][0]["ProjectName"]
            log.info(f"Using project {project_name}")
            return project_name
        except IndexError as e:
            raise IndexError(f"No projects found boto3 error: {e}")

    def get_first_model_version(self) -> str:
        """get first model version"""
        response = self.client.list_models(ProjectName=self.project_name)
        model_version = response["Models"][0]["ModelVersion"]
        try:
            log.info(f"Using model version {model_version}")
            return model_version
        except IndexError as e:
            raise IndexError(f"No models found for project {self.project_name} with error: {e}")

    def start_model(self):
        """start model"""
        if self.get_model_status() == "STARTING_HOSTING":
            log.info(
                f"Model {self.project_name} with model {self.model_version} is already STARTING_HOSTING, so no need starting it"
            )
            return True
        self.client.start_model(ProjectName=self.project_name, ModelVersion="1", MinInferenceUnits=1)
        return True

    def stop_model(self):
        """stop model"""
        if self.get_model_status() == "HOSTED":
            self.client.stop_model(ProjectName=self.project_name, ModelVersion="1")
        else:
            log.info(f"Model {self.project_name} with model {self.model_version} is not HOSTED, so no need stopping it")
        return True

    def get_model_status(self):
        """get model status message"""
        return self.client.list_models(ProjectName=self.project_name)["Models"][0]["Status"]
