from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
    aws_ecr_assets as ecr_assets,
)
from constructs import Construct

class SurveyPlaywrightStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        image = ecr_assets.DockerImageAsset(
            self,
            "SurveyPlaywrightImage",
            directory=".",  # root where Dockerfile lives
        )

        _lambda.DockerImageFunction(
            self,
            "SurveyPlaywrightLambda",
            code=_lambda.DockerImageCode.from_ecr(
                repository=image.repository,
                tag=image.image_uri.split(":")[-1],
            ),
            memory_size=2048,
            timeout=Duration.seconds(90),
        )