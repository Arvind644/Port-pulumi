"""A Python Pulumi program"""

import pulumi
import port

config = pulumi.Config()
ENVIRONMENT = pulumi.get_stack()
BUCKET_ACL = config.get("bucketAcl") or "private"

# Create S3 blueprint
s3_bucket_blueprint = port.PortBlueprint(
    "s3Bucket",
    "S3 Bucket",
    "AWS",
    [
        {
            "identifier": "acl",
            "title": "Bucket ACL",
            "required": False,
            "type": "string",
        },
        {
            "identifier": "url",
            "title": "Bucket URL",
            "required": False,
            "type": "string",
            "format": "url",
        },
    ],
    [],
    [],
    [],
)

pulumi.export(
    f"s3Bucket blueprint identifier", s3_bucket_blueprint.blueprint.identifier
)

# Create SQS blueprint
sqs_blueprint = port.PortBlueprint(
    "sqsQueue",
    "SQS Queue",
    "AWS",
    [
        {
            "identifier": "url",
            "title": "Queue URL",
            "required": False,
            "type": "string",
            "format": "url",
        },
    ],
    [],
    [],
    [],
)

pulumi.export(f"sqsQueue blueprint identifier", sqs_blueprint.blueprint.identifier)

# Create Lambda blueprint
lambda_blueprint = port.PortBlueprint(
    "lambda",
    "Lambda",
    "Lambda",
    [
        {
            "identifier": "url",
            "title": "Lambda URL",
            "required": False,
            "type": "string",
            "format": "url",
        },
        {
            "identifier": "memory",
            "title": "Memory Size",
            "required": False,
            "type": "number",
        },
    ],
    [],
    [],
    [],
)

pulumi.export(f"Lambda blueprint identifier", lambda_blueprint.blueprint.identifier)

# Create DevEnv blueprint
dev_env_blueprint = port.PortBlueprint(
    "devEnv",
    "Developer Environment",
    "Environment",
    [
        {
            "identifier": "env",
            "title": "Environment",
            "type": "string",
            "default": "dev",
        },
    ],
    [
        {
            "target": lambda_blueprint.blueprint.identifier,
            "title": "Lambda",
            "identifier": "lambda",
            "many": False,
            "required": False,
        },
        {
            "target": s3_bucket_blueprint.blueprint.identifier,
            "title": "S3 Bucket",
            "identifier": "s3Bucket",
            "many": False,
            "required": False,
        },
        {
            "target": sqs_blueprint.blueprint.identifier,
            "title": "SQS Queue",
            "identifier": "sqsQueue",
            "many": False,
            "required": False,
        },
    ],
    [],
    [],
    opts=pulumi.ResourceOptions(
        depends_on=[
            lambda_blueprint.blueprint,
            s3_bucket_blueprint.blueprint,
            sqs_blueprint.blueprint,
        ]
    ),
)

pulumi.export(f"DevEnv blueprint identifier", dev_env_blueprint.blueprint.identifier)

deploy_stack_action = port.PortAction(
    "devEnv",
    "deployStack",
    "Deploy Stack in Env",
    "Pulumi",
    "Deploys the Pulumi stack in a new environment",
    [{"identifier": "stackName", "type": "string", "title": "Stack Name"}],
    "CREATE",
    {
        "type": "GITHUB",
        "org": "port-live-webinar",
        "repo": "pulumi-dev-env",
        "workflow": "pulumi_deploy.yml",
        "omitPayload": False,
        "omitUserInputs": True,
    },
    opts=pulumi.ResourceOptions(
        depends_on=[
            dev_env_blueprint.blueprint,
        ]
    ),
)

deploy_stack_action = port.PortAction(
    "devEnv",
    "teardownStack",
    "Teardown Stack in Env",
    "Pulumi",
    "Destroys the Pulumi stack in a new environment",
    [],
    "DELETE",
    {
        "type": "GITHUB",
        "org": "port-live-webinar",
        "repo": "pulumi-dev-env",
        "workflow": "pulumi_destroy.yml",
        "omitPayload": False,
        "omitUserInputs": True,
    },
    opts=pulumi.ResourceOptions(
        depends_on=[
            dev_env_blueprint.blueprint,
        ]
    ),
)