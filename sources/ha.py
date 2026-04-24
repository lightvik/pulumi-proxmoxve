import pulumi
import pulumi_proxmoxve as proxmox

from models import HaGroupSpec, MergedVMSpec


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
    vm_spec: MergedVMSpec,
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
