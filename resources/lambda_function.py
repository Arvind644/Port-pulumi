from typing import Optional
import json
from pulumi import ComponentResource, Output, ResourceOptions
import pulumi
from pulumi.output import Inputs
from pulumi.resource import ResourceOptions
from pulumi_aws import iam, lambda_
from port_pulumi import Entity


class LambdaFunction(ComponentResource):
    blueprint_id = "lambda"
    runtime = "nodejs16.x"
    lambda_handler = "index.handler"

    def __init__(
        self,
        lambda_name: str,
        props: dict | None = None,
        opts: ResourceOptions | None = None,
        dependencies: list | None = None,
    ) -> None:
        super().__init__(
            f"pulumi-webinar:lambda:lambda:{lambda_name}", lambda_name, props, opts
        )
        self.create_role(lambda_name)
        self.create_lambda(lambda_name, props)
        self.create_lambda_url(lambda_name)
        self.create_lambda_entity(
            self.blueprint_id,
            self.lambda_function.arn,
            self.lambda_function.name,
            {"memory": self.lambda_function.memory_size},
            dependencies,
        )

    def create_role(self, name):
        child_opts = ResourceOptions(parent=self)
        self.lambda_role = iam.Role(
            "lambda_role",
            assume_role_policy=Output.from_input(
                """
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "sts:AssumeRole",
                    "Principal": {"Service": "lambda.amazonaws.com"},
                    "Effect": "Allow",
                    "Sid": ""
                }
            ]
        }
        """
            ),
            description="Port Pulumi webinar Lambda Role",
            opts=child_opts,
        )

        # Attach the AWS managed policy for Lambda execution to the role
        assume_role_policy_attachment = iam.RolePolicyAttachment(
            "lambda_role_policy_attachment",
            policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
            role=self.lambda_role.name,
            opts=child_opts,
        )

        # # Export role Amazon Resource Name (ARN)
        # self.register_outputs({"lambda_role_arn", self.lambda_role.arn})

    def create_lambda(self, name, props):
        # This definition ensures the new component resource acts like anything else in the Pulumi ecosystem when being called in code.
        child_opts = ResourceOptions(parent=self)
        self.name = name
        self.lambda_name = f"{self.name}-lambda"
        self.lambda_function = lambda_.Function(
            self.lambda_name,
            runtime=self.runtime,
            role=self.lambda_role.arn,
            handler=self.lambda_handler,
            code=pulumi.AssetArchive({".": pulumi.FileArchive("./sample_lambda_code")}),
            opts=child_opts,
        )
        # We also need to register all the expected outputs for this component resource that will get returned by default.
        self.register_outputs(
            {
                "lambda_function_name": self.lambda_function.name,
                "lambda_function_arn": self.lambda_function.arn,
                "lambda_function_version": self.lambda_function.version,
            }
        )

    def create_lambda_url(self, name):
        child_opts = ResourceOptions(parent=self)
        self.lambda_url = lambda_.FunctionUrl(
            name,
            function_name=self.lambda_function.name,
            authorization_type="NONE",
            cors=lambda_.FunctionUrlCorsArgs(
                allow_credentials=True,
                allow_origins=["*"],
                allow_methods=["*"],
                allow_headers=[
                    "date",
                    "keep-alive",
                ],
                expose_headers=[
                    "keep-alive",
                    "date",
                ],
                max_age=86400,
            ),
            opts=child_opts,
        )

    def create_lambda_entity(self, blueprint_id, lambda_id, title, props, dependencies):
        child_opts = ResourceOptions(parent=self, depends_on=dependencies)
        self.lambda_function_entity = Entity(
            self.lambda_name,
            opts=child_opts,
            identifier=self.lambda_name,
            title=title,
            blueprint=blueprint_id,
            properties=[
                {
                    "name": "url",
                    "value": self.lambda_url.function_url,
                },
                {"name": "memory", "value": self.lambda_function.memory_size},
            ],
            relations=[],
        )