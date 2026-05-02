import pulumi
import pulumi_proxmoxve as proxmox

from models import NetworkBridgeSpec, NetworkVlanSpec


def build_linux_bridge(
    spec: NetworkBridgeSpec,
    provider: proxmox.Provider,
) -> proxmox.network.linux.Bridge:
    args: dict = {"node_name": spec.node, "name": spec.name}
    if spec.address is not None:
        args["address"] = spec.address
    if spec.address6 is not None:
        args["address6"] = spec.address6
    if spec.autostart is not None:
        args["autostart"] = spec.autostart
    if spec.comment is not None:
        args["comment"] = spec.comment
    if spec.gateway is not None:
        args["gateway"] = spec.gateway
    if spec.gateway6 is not None:
        args["gateway6"] = spec.gateway6
    if spec.mtu is not None:
        args["mtu"] = spec.mtu
    if spec.ports is not None:
        args["ports"] = spec.ports
    if spec.timeout_reload is not None:
        args["timeout_reload"] = spec.timeout_reload
    if spec.vlan_aware is not None:
        args["vlan_aware"] = spec.vlan_aware

    return proxmox.network.linux.Bridge(
        f"bridge-{spec.node}-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_linux_vlan(
    spec: NetworkVlanSpec,
    provider: proxmox.Provider,
) -> proxmox.network.linux.Vlan:
    args: dict = {"node_name": spec.node, "name": spec.name}
    if spec.address is not None:
        args["address"] = spec.address
    if spec.address6 is not None:
        args["address6"] = spec.address6
    if spec.autostart is not None:
        args["autostart"] = spec.autostart
    if spec.comment is not None:
        args["comment"] = spec.comment
    if spec.gateway is not None:
        args["gateway"] = spec.gateway
    if spec.gateway6 is not None:
        args["gateway6"] = spec.gateway6
    if spec.interface is not None:
        args["interface"] = spec.interface
    if spec.mtu is not None:
        args["mtu"] = spec.mtu
    if spec.timeout_reload is not None:
        args["timeout_reload"] = spec.timeout_reload
    if spec.vlan is not None:
        args["vlan"] = spec.vlan

    return proxmox.network.linux.Vlan(
        f"vlan-{spec.node}-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )
