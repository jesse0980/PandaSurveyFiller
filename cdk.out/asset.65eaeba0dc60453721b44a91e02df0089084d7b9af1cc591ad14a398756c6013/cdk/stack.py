import aws_cdk as cdk
from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    aws_apigateway as apigw,
    aws_iam as iam,
)
from constructs import Construct


class SurveyPlaywrightStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # 1. Playwright Lambda (Docker)
        playwright_lambda = _lambda.DockerImageFunction(
            self,
            "SurveyPlaywrightLambda",
            code=_lambda.DockerImageCode.from_image_asset(directory="."),
            memory_size=2048,
            timeout=Duration.seconds(90),
        )

        # 2. Step Function (with retry)
        task = tasks.LambdaInvoke(
            self,
            "ExecutePlaywright",
            lambda_function=playwright_lambda,
            output_path="$.Payload",
        ).add_retry(
            max_attempts=2,
            interval=Duration.seconds(5),
        )

        state_machine = sfn.StateMachine(
            self,
            "SurveyStateMachine",
            definition=task,
            state_machine_type=sfn.StateMachineType.STANDARD,
            timeout=Duration.minutes(5),
        )

        # 3. API Gateway
        api = apigw.RestApi(
            self,
            "SurveyApi",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
            ),
        )

        # ✅ FIXED IAM ROLE
        api_role = iam.Role(
            self,
            "ApiGatewayStepFunctionsRole",
            assumed_by=iam.ServicePrincipal("apigateway.amazonaws.com"),
        )

        state_machine.grant_start_execution(api_role)
        state_machine.grant_read(api_role)

        # ---------------------------
        # 4. REQUEST VALIDATION MODEL
        # ---------------------------
        request_model = apigw.Model(
            self,
            "StartRequestModel",
            rest_api=api,
            content_type="application/json",
            schema=apigw.JsonSchema(
                type=apigw.JsonSchemaType.OBJECT,
                required=["email"],
                properties={
                    "email": apigw.JsonSchema(
                        type=apigw.JsonSchemaType.STRING,
                        format="email",
                    )
                },
            ),
        )

        validator = apigw.RequestValidator(
            self,
            "StartRequestValidator",
            rest_api=api,
            validate_request_body=True,
        )

        # ---------------------------
        # 5. POST /start (email required)
        # ---------------------------
        start_resource = api.root.add_resource("start")

        start_resource.add_method(
            "POST",
            apigw.StepFunctionsIntegration.start_execution(
                state_machine,
                credentials_role=api_role,
                request_templates={
                    "application/json": """
                    {
                      "input": "$util.escapeJavaScript($input.body)"
                    }
                    """
                },
                integration_responses=[{
                    "statusCode": "200",
                    "responseParameters": {
                        "method.response.header.Access-Control-Allow-Origin": "'*'"
                    }
                }],
            ),
            request_models={
                "application/json": request_model
            },
            request_validator=validator,
            method_responses=[{
                "statusCode": "200",
                "responseParameters": {
                    "method.response.header.Access-Control-Allow-Origin": True
                }
            }],
        )

        # ---------------------------
        # 6. GET /status
        # ---------------------------
        status_resource = api.root.add_resource("status")

        status_resource.add_method(
            "GET",
            apigw.AwsIntegration(
                service="states",
                action="DescribeExecution",
                options=apigw.IntegrationOptions(
                    credentials_role=api_role,
                    request_templates={
                        "application/json": '{"executionArn": "$method.request.querystring.executionArn"}'
                    },
                    integration_responses=[{
                        "statusCode": "200",
                        "responseParameters": {
                            "method.response.header.Access-Control-Allow-Origin": "'*'"
                        }
                    }],
                ),
            ),
            request_parameters={
                "method.request.querystring.executionArn": True
            },
            method_responses=[{
                "statusCode": "200",
                "responseParameters": {
                    "method.response.header.Access-Control-Allow-Origin": True
                }
            }],
        )