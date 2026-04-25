import aws_cdk as cdk
from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
)
from constructs import Construct


class SurveyPlaywrightStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # -------------------------
        # 1. WORKER LAMBDA (PLAYWRIGHT - HEAVY)
        # -------------------------
        worker_lambda = _lambda.DockerImageFunction(
            self,
            "WorkerLambda",
            code=_lambda.DockerImageCode.from_image_asset(
                directory="worker"   # 👈 Docker Playwright folder
            ),
            memory_size=2048,
            timeout=Duration.seconds(90),
        )

        # -------------------------
        # 2. API LAMBDA (VALIDATION + TRIGGER)
        # -------------------------
        api_lambda = _lambda.Function(
            self,
            "ApiLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.handler",
            code=_lambda.Code.from_asset("api"),
            timeout=Duration.seconds(10),
            environment={
                "WORKER_FUNCTION_NAME": worker_lambda.function_name,
            },
        )

        # Allow API Lambda to invoke Worker Lambda
        worker_lambda.grant_invoke(api_lambda)

        # -------------------------
        # 3. API GATEWAY
        # -------------------------
        api = apigw.RestApi(
            self,
            "SurveyApi",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
            ),
        )

        # -------------------------
        # 4. POST /start
        # -------------------------
        start_resource = api.root.add_resource("start")

        start_resource.add_method(
            "POST",
            apigw.LambdaIntegration(api_lambda, proxy=True)
        )