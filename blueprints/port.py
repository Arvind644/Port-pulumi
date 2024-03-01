from pulumi import ComponentResource, ResourceOptions, Output
from port_pulumi import Blueprint, Entity, Action


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


class PortAction(ComponentResource):
    def __init__(
        self,
        blueprint_id: str,
        action_id: str,
        title: str,
        icon: str,
        description: str = "",
        user_inputs: dict | None = None,
        trigger: str = "CREATE",
        #invocation_method: dict | None = None,
        props: dict | None = None,
        opts: ResourceOptions | None = None,
    ) -> None:
        super().__init__(
            f"pulumi-webinar:port:blueprint:{blueprint_id}:action:{action_id}",
            action_id,
            props,
            opts,
        )
        self.create_action(
            blueprint_id,
            action_id,
            title,
            icon,
            description,
            user_inputs,
            trigger,
           # invocation_method,
        )

    def create_action(
        self,
        blueprint_id,
        action_id,
        title,
        icon,
        description,
        user_inputs,
        trigger,
       # invocation_method,
    ):
        # This definition ensures the new component resource acts like anything else in the Pulumi ecosystem when being called in code.
        child_opts = ResourceOptions(parent=self)
        self.blueprint = Action(
            action_id,
            blueprint=blueprint_id,
            identifier=action_id,
            title=title,
            icon=icon,
            description=description,
            user_properties=user_inputs,
            trigger=trigger,
          #  invocation_method=invocation_method,
            opts=child_opts,
        )

        self.register_outputs({f"{action_id}-identifier": action_id})


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