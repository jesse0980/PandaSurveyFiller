from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
)
from constructs import Construct

class SurveyPlaywrightStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        _lambda.DockerImageFunction(
            self,
            "SurveyPlaywrightLambda",
            code=_lambda.DockerImageCode.from_image_asset(
                directory=".",  # where Dockerfile lives
            ),
            memory_size=2048,
            timeout=Duration.seconds(90),
        )