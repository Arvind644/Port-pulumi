from pulumi import ComponentResource, ResourceOptions, Output
from port_pulumi import Blueprint, Entity


class PortBlueprint(ComponentResource):
    def __init__(
        self,
        blueprint_id: str,
        title: str,
        icon: str,
        properties: dict | None = None,
        relations: dict | None = None,
        mirror_properties: dict | None = None,
        calculation_properties: dict | None = None,
        props: dict | None = None,
        opts: ResourceOptions | None = None,
    ) -> None:
        super().__init__(
            f"pulumi-webinar:port:blueprint:{blueprint_id}",
            blueprint_id,
            props,
            opts,
        )
        self.create_blueprint(
            blueprint_id,
            title,
            icon,
            properties,
            relations,
            mirror_properties,
            calculation_properties,
        )

    def create_blueprint(
        self,
        blueprint_id,
        title,
        icon,
        properties,
        relations,
        mirror_properties,
        calculation_properties,
    ):
        # This definition ensures the new component resource acts like anything else in the Pulumi ecosystem when being called in code.
        child_opts = ResourceOptions(parent=self)
        self.blueprint = Blueprint(
            blueprint_id,
            opts=child_opts,
            identifier=blueprint_id,
            title=title,
            icon=icon,
            properties=properties,
            relations=relations,
            mirror_properties=mirror_properties,
            calculation_properties=calculation_properties,
        )

        self.register_outputs({f"{blueprint_id}-identifier": blueprint_id})


class PortEntity(ComponentResource):
    def __init__(
        self,
        blueprint_id: str,
        identifier: str,
        title: str,
        properties: dict | None = None,
        relations: dict | None = None,
        props: dict | None = None,
        opts: ResourceOptions | None = None,
        dependencies: list | None = None,
    ) -> None:
        super().__init__(
            f"pulumi-webinar:port:blueprint:{blueprint_id}:{identifier}",
            blueprint_id,
            props,
            opts,
        )
        self.create_port_entity(
            blueprint_id,
            identifier,
            title,
            properties,
            relations,
            dependencies=dependencies,
        )

    def create_port_entity(
        self, blueprint_id, identifier, title, props, relations, dependencies
    ):
        child_opts = ResourceOptions(parent=self, depends_on=dependencies)
        self.dev_env_entity = Entity(
            title,
            opts=child_opts,
            identifier=identifier,
            title=title,
            blueprint=blueprint_id,
            properties=props,
            relations=relations,
        )