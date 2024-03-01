from typing import Optional
import json
from pulumi import ComponentResource, Output, ResourceOptions
from pulumi.output import Inputs
from pulumi.resource import ResourceOptions
from pulumi_aws import sqs
from port_pulumi import Entity


class SqsQueue(ComponentResource):
    blueprint_id = "sqsQueue"

    def __init__(
        self,
        queue_name: str,
        props: dict | None = None,
        opts: ResourceOptions | None = None,
        dependencies: list | None = None,
    ) -> None:
        super().__init__(
            f"pulumi-webinar:sqsQueue:queue:{queue_name}", queue_name, props, opts
        )
        self.create_queue(queue_name, props)

        self.create_queue_entity(
            self.blueprint_id,
            self.queue.arn,
            self.queue.name,
            {"url": self.queue.url},
            dependencies,
        )

    def create_queue(self, name, props):
        # This definition ensures the new component resource acts like anything else in the Pulumi ecosystem when being called in code.
        child_opts = ResourceOptions(parent=self)
        self.name = name
        self.queue_name = f"{self.name}-queue"
        self.queue = sqs.Queue(self.queue_name, child_opts)
        # We also need to register all the expected outputs for this component resource that will get returned by default.
        self.register_outputs(
            {
                "queue_name": self.queue.name,
                "queue_id": self.queue.id,
                "queue_arn": self.queue.arn,
            }
        )

    def create_queue_entity(self, blueprint_id, queue_id, title, props, dependencies):
        child_opts = ResourceOptions(parent=self, depends_on=dependencies)
        self.sqs_queue_entity = Entity(
            self.queue_name,
            opts=child_opts,
            identifier=self.queue_name,
            title=title,
            blueprint=blueprint_id,
            properties=[
                {
                    "name": "url",
                    "value": Output.all(props["url"]).apply(
                        lambda inputs: f"{inputs[0]}"
                    ),
                },
            ],
            relations=[],
        )