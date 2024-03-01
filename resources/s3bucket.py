from typing import Optional
import json
from pulumi import ComponentResource, Output, ResourceOptions
from pulumi.output import Inputs
from pulumi.resource import ResourceOptions
from pulumi_aws import s3
from port_pulumi import Entity


class S3Bucket(ComponentResource):
    blueprint_id = "s3Bucket"

    def __init__(
        self,
        bucket_name: str,
        props: dict | None = None,
        opts: ResourceOptions | None = None,
        dependencies: list | None = None,
    ) -> None:
        super().__init__(
            f"pulumi-webinar:s3bucket:bucket:{bucket_name}", bucket_name, props, opts
        )
        self.create_bucket(bucket_name, props)

        self.create_bucket_entity(
            self.blueprint_id,
            self.bucket.id,
            self.bucket.id,
            {"acl": props["acl"], "url": self.bucket.bucket_domain_name},
            dependencies,
        )

    def create_bucket(self, name, props):
        # This definition ensures the new component resource acts like anything else in the Pulumi ecosystem when being called in code.
        child_opts = ResourceOptions(parent=self)
        self.name = name
        self.bucket_name = f"{self.name}-bucket"
        self.bucket = s3.Bucket(self.bucket_name, child_opts, acl=props["acl"])
        # We also need to register all the expected outputs for this component resource that will get returned by default.
        self.register_outputs({"bucket_name": self.bucket.id})

    def create_bucket_entity(self, blueprint_id, bucket_id, title, props, dependencies):
        child_opts = ResourceOptions(parent=self, depends_on=dependencies)
        self.bucket_entity = Entity(
            self.bucket_name,
            opts=child_opts,
            identifier=Output.all(bucket_id).apply(lambda inputs: f"{inputs[0]}"),
            title=title,
            blueprint=blueprint_id,
            properties=[
                {"name": "acl", "value": props["acl"]},
                {
                    "name": "url",
                    "value": Output.all(props["url"]).apply(
                        lambda inputs: f"https://{inputs[0]}"
                    ),
                },
            ],
            relations=[],
        )

    # def define_policy(self):
    #     policy_name = self.policy_name
    #     try:
    #         json_data = self.policy_list[f"{policy_name}"]
    #         policy = self.bucket.arn.apply(lambda arn: json.dumps(json_data).replace('fakeobjectresourcething', arn))
    #         return policy
    #     except KeyError as err:
    #         add_note = "Policy name needs to be 'default', 'locked', or 'permissive'"
    #         print(f"Error: {add_note}. You used {policy_name}.")
    #         raise

    # def set_policy(self):
    #     bucket_policy = aws_classic.s3.BucketPolicy(
    #         f"{self.name_me}-policy",
    #         bucket=self.bucket.id,
    #         policy=self.define_policy(),
    #         opts=pulumi.ResourceOptions(parent=self.bucket)
    #     )
    #     return bucket_policy