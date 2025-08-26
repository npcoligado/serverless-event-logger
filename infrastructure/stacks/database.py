import os

from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_dynamodb as dynamodb,
)
from constructs import Construct


class DatabaseStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        removal_policy = (
            RemovalPolicy.RETAIN
            if os.environ["STAGE"] == "production"
            else RemovalPolicy.DESTROY
        )

        self.events_table = dynamodb.TableV2(
            self,
            "events",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING,
            ),
            billing=dynamodb.Billing.on_demand(),
            removal_policy=removal_policy,
        )
