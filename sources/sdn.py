import pulumi
import pulumi_proxmoxve as proxmox

from models import (
    SdnZoneSpec,
    SdnVnetSpec,
    SdnSubnetSpec,
    SdnApplierSpec,
    SdnFabricOpenfabricSpec,
    SdnFabricOspfSpec,
    SdnFabricNodeOpenfabricSpec,
    SdnFabricNodeOspfSpec,
)

_ZONE_CLASSES = {
    "simple": proxmox.sdn.zone.Simple,
    "vxlan":  proxmox.sdn.zone.Vxlan,
    "vlan":   proxmox.sdn.zone.Vlan,
    "evpn":   proxmox.sdn.zone.Evpn,
    "qinq":   proxmox.sdn.zone.Qinq,
}


def build_sdn_zone(
    spec: SdnZoneSpec,
    provider: proxmox.Provider,
) -> pulumi.CustomResource:
    zone_cls = _ZONE_CLASSES.get(spec.type)
    if zone_cls is None:
        raise ValueError(f"Unknown SDN zone type: '{spec.type}'. Supported: {list(_ZONE_CLASSES)}")

    args: dict = {"resource_id": spec.name}
    if spec.mtu is not None:
        args["mtu"] = spec.mtu
    if spec.nodes:
        args["nodes"] = spec.nodes

    return zone_cls(
        f"sdn-zone-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_sdn_vnet(
    spec: SdnVnetSpec,
    zone: pulumi.CustomResource,
    provider: proxmox.Provider,
) -> proxmox.sdn.Vnet:
    args: dict = {
        "resource_id": spec.name,
        "zone": spec.zone,
    }
    if spec.tag is not None:
        args["tag"] = spec.tag
    if spec.vlan_aware is not None:
        args["vlan_aware"] = spec.vlan_aware

    return proxmox.sdn.Vnet(
        f"sdn-vnet-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider, depends_on=[zone]),
    )


def build_sdn_subnet(
    spec: SdnSubnetSpec,
    vnet: proxmox.sdn.Vnet,
    provider: proxmox.Provider,
) -> proxmox.sdn.Subnet:
    args: dict = {
        "cidr": spec.cidr,
        "vnet": spec.vnet,
    }
    if spec.gateway:
        args["gateway"] = spec.gateway
    if spec.snat is not None:
        args["snat"] = spec.snat

    return proxmox.sdn.Subnet(
        f"sdn-subnet-{spec.cidr.replace('/', '-')}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider, depends_on=[vnet]),
    )


def build_sdn_applier(
    spec: SdnApplierSpec,
    provider: proxmox.Provider,
) -> pulumi.CustomResource:
    args: dict = {}
    if spec.on_create is not None:
        args["on_create"] = spec.on_create
    if spec.on_destroy is not None:
        args["on_destroy"] = spec.on_destroy

    cls = proxmox.sdn.ApplierLegacy if spec.legacy else proxmox.sdn.Applier
    return cls("sdn-applier", **args, opts=pulumi.ResourceOptions(provider=provider))


def build_sdn_fabric_openfabric(
    spec: SdnFabricOpenfabricSpec,
    provider: proxmox.Provider,
) -> pulumi.CustomResource:
    args: dict = {"resource_id": spec.name}
    if spec.csnp_interval is not None:
        args["csnp_interval"] = spec.csnp_interval
    if spec.hello_interval is not None:
        args["hello_interval"] = spec.hello_interval
    if spec.ip6_prefix is not None:
        args["ip6_prefix"] = spec.ip6_prefix
    if spec.ip_prefix is not None:
        args["ip_prefix"] = spec.ip_prefix

    cls = proxmox.sdn.fabric.OpenfabricLegacy if spec.legacy else proxmox.sdn.fabric.Openfabric
    return cls(
        f"sdn-fabric-openfabric-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_sdn_fabric_ospf(
    spec: SdnFabricOspfSpec,
    provider: proxmox.Provider,
) -> pulumi.CustomResource:
    args: dict = {
        "resource_id": spec.name,
        "area": spec.area,
        "ip_prefix": spec.ip_prefix,
    }

    cls = proxmox.sdn.fabric.OspfLegacy if spec.legacy else proxmox.sdn.fabric.Ospf
    return cls(
        f"sdn-fabric-ospf-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_sdn_fabric_node_openfabric(
    spec: SdnFabricNodeOpenfabricSpec,
    fabric: pulumi.CustomResource,
    provider: proxmox.Provider,
) -> pulumi.CustomResource:
    args: dict = {
        "fabric_id": spec.fabric_id,
        "node_id": spec.node_id,
        "interface_names": spec.interface_names,
    }
    if spec.ip is not None:
        args["ip"] = spec.ip
    if spec.ip6 is not None:
        args["ip6"] = spec.ip6

    cls = proxmox.sdn.fabric.node.OpenfabricLegacy if spec.legacy else proxmox.sdn.fabric.node.Openfabric
    return cls(
        f"sdn-fabric-node-openfabric-{spec.fabric_id}-{spec.node_id}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider, depends_on=[fabric]),
    )


def build_sdn_fabric_node_ospf(
    spec: SdnFabricNodeOspfSpec,
    fabric: pulumi.CustomResource,
    provider: proxmox.Provider,
) -> pulumi.CustomResource:
    args: dict = {
        "fabric_id": spec.fabric_id,
        "node_id": spec.node_id,
        "interface_names": spec.interface_names,
        "ip": spec.ip,
    }

    cls = proxmox.sdn.fabric.node.OspfLegacy if spec.legacy else proxmox.sdn.fabric.node.Ospf
    return cls(
        f"sdn-fabric-node-ospf-{spec.fabric_id}-{spec.node_id}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider, depends_on=[fabric]),
    )
