"""An AWS Python Pulumi program"""

import pulumi
import s3bucket
import sqs
import port
import lambda_function
from pulumi.output import Inputs

config = pulumi.Config()
ENVIRONMENT = pulumi.get_stack()
BUCKET_ACL = config.get("bucketAcl") or "private"

BUCKET_BLUEPRINT_IDENTIFIER = "s3Bucket"
QUEUE_BLUEPRINT_IDENTIFIER = "sqsQueue"
LAMBDA_BLUEPRINT_IDENTIFIER = "lambda"
DEVENV_BLUEPRINT_IDENTIFIER = "devEnv"

# Create a new bucket
bucket = s3bucket.S3Bucket(
    f"port-pulumi-webinar-{ENVIRONMENT}",
    {"acl": BUCKET_ACL},
)

pulumi.export("Bucket Name", bucket.bucket.id)

# Create a new SQS queue
queue = sqs.SqsQueue(f"port-pulumi-webinar-{ENVIRONMENT}")
pulumi.export("Queue Name", queue.queue.name)

# Create a new Lambda function
lambda_function = lambda_function.LambdaFunction(f"port-pulumi-webinar-{ENVIRONMENT}")
pulumi.export("Lambda Name", lambda_function.lambda_function.name)

# Create a new dev-env entity
dev_env_entity = port.PortEntity(
    "devEnv",
    f"port-pulumi-webinar-{ENVIRONMENT}-dev-env",
    f"Port Pulumi Webinar {ENVIRONMENT} Developer Environment",
    properties=[
        {
            "name": "env",
            "value": f"{ENVIRONMENT}",
        },
    ],
    relations=[
        {
            "name": "lambda",
            "identifier": lambda_function.lambda_function_entity.identifier,
        },
        {"name": "s3Bucket", "identifier": bucket.bucket_entity.identifier},
        {"name": "sqsQueue", "identifier": queue.sqs_queue_entity.identifier},
    ],
    dependencies=[
        bucket.bucket,
        queue.queue,
        lambda_function.lambda_function,
    ],
)