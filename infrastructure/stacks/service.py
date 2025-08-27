import os

from aws_cdk import (
    Stack,
    Duration,
    aws_apigateway as apigateway,
    aws_iam as iam,
    aws_lambda as lambda_,
)
from aws_cdk.aws_lambda_python_alpha import PythonFunction, BundlingOptions
from constructs import Construct
from pathlib import Path

from stacks.database import DatabaseStack


class ServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, database_stack: DatabaseStack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        root_path = Path(__file__).parent.parent.parent

        self.service_function = PythonFunction(
            self,
            "eventLoggerFunction",
            entry=str(root_path.resolve()),
            runtime=lambda_.Runtime.PYTHON_3_13,
            index="app/main.py",
            handler="handler",
            timeout=Duration.seconds(30),
            memory_size=512,
            environment={
                "ENV": os.environ["STAGE"],
                "EVENTS_TABLE": database_stack.events_table.table_name,
            },
            bundling=BundlingOptions(
                asset_excludes=[
                    ".venv/**",
                    "**__pycache__/**",
                    "local-env.bat",
                ],
                image=lambda_.Runtime.PYTHON_3_13.bundling_image,
                command=[
                    "bash", "-c",
                    "pip install --target /asset-output ."
                ],
            ),
        )

        
        self.service_function.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "dynamodb:GetItem",
                    "dynamodb:PutItem",
                ],
                resources=[database_stack.events_table.table_arn]
            )
        )

        self.api = apigateway.LambdaRestApi(
            self,
            "api",
            handler=self.service_function,
            proxy=True,
            deploy_options=apigateway.StageOptions(stage_name=os.environ['STAGE']),
        )
