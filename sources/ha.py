import pulumi
import pulumi_proxmoxve as proxmox

from models import HaGroupSpec, HaRuleSpec, VMSpec


def build_ha_group(
    spec: HaGroupSpec,
    provider: proxmox.Provider,
) -> proxmox.HagroupLegacy:
    nodes = (
        [
            proxmox.HagroupLegacyNodeArgs(
                node=n.node,
                priority=n.priority,
            )
            for n in spec.nodes
        ]
        if spec.nodes
        else None
    )
    return proxmox.HagroupLegacy(
        f"ha-group-{spec.name}",
        group=spec.name,
        comment=spec.comment,
        restricted=spec.restricted,
        no_failback=spec.no_failback,
        nodes=nodes,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_ha_resource(
    vm_spec: VMSpec,
    vm: proxmox.VmLegacy,
    provider: proxmox.Provider,
) -> proxmox.HaresourceLegacy:
    ha = vm_spec.ha
    args: dict = {
        "resource_id": f"vm:{vm_spec.vmid}",
        "state": ha.state,
    }
    if ha.group:
        args["group"] = ha.group
    if ha.max_restart is not None:
        args["max_restart"] = ha.max_restart
    if ha.max_relocate is not None:
        args["max_relocate"] = ha.max_relocate
    if ha.comment:
        args["comment"] = ha.comment

    return proxmox.HaresourceLegacy(
        f"ha-resource-{vm_spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider, depends_on=[vm]),
    )


def build_ha_rule(
    spec: HaRuleSpec,
    provider: proxmox.Provider,
) -> proxmox.HaruleLegacy:
    args: dict = {}
    if spec.resource_id is not None:
        args["resource_id"] = spec.resource_id
    if spec.affinity is not None:
        args["affinity"] = spec.affinity
    if spec.comment is not None:
        args["comment"] = spec.comment
    if spec.disable is not None:
        args["disable"] = spec.disable
    if spec.nodes is not None:
        args["nodes"] = spec.nodes
    if spec.resources is not None:
        args["resources"] = spec.resources
    if spec.rule is not None:
        args["rule"] = spec.rule
    if spec.strict is not None:
        args["strict"] = spec.strict
    if spec.type is not None:
        args["type"] = spec.type

    return proxmox.HaruleLegacy(
        f"ha-rule-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )
