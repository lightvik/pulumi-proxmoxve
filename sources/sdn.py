import pulumi
import pulumi_proxmoxve as proxmox

from models import SdnZoneSpec, SdnVnetSpec, SdnSubnetSpec

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
