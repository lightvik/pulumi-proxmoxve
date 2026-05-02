import pulumi
import pulumi_proxmoxve as proxmox

from models import ReplicationSpec


def build_replication(
    spec: ReplicationSpec,
    provider: proxmox.Provider,
) -> proxmox.Replication:
    args: dict = {}
    if spec.resource_id is not None:
        args["resource_id"] = spec.resource_id
    if spec.target is not None:
        args["target"] = spec.target
    if spec.schedule is not None:
        args["schedule"] = spec.schedule
    if spec.comment is not None:
        args["comment"] = spec.comment
    if spec.disable is not None:
        args["disable"] = spec.disable
    if spec.rate is not None:
        args["rate"] = spec.rate
    if spec.type is not None:
        args["type"] = spec.type

    return proxmox.Replication(
        f"replication-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )
