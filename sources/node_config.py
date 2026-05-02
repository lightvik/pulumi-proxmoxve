import pulumi
import pulumi_proxmoxve as proxmox

from models import NodeDnsSpec, NodeHostsSpec, NodeTimeSpec


def build_dns(
    spec: NodeDnsSpec,
    provider: proxmox.Provider,
) -> proxmox.DnsLegacy:
    args: dict = {"node_name": spec.node, "servers": spec.servers}
    if spec.domain is not None:
        args["domain"] = spec.domain

    return proxmox.DnsLegacy(
        f"dns-{spec.node}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_hosts(
    spec: NodeHostsSpec,
    provider: proxmox.Provider,
) -> proxmox.HostsLegacy:
    entries = [
        proxmox.HostsLegacyEntryArgs(
            address=e.address,
            hostnames=e.hostnames,
        )
        for e in spec.entries
    ]

    return proxmox.HostsLegacy(
        f"hosts-{spec.node}",
        node_name=spec.node,
        entry=entries,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_time(
    spec: NodeTimeSpec,
    provider: proxmox.Provider,
) -> proxmox.TimeLegacy:
    return proxmox.TimeLegacy(
        f"time-{spec.node}",
        node_name=spec.node,
        time_zone=spec.time_zone,
        opts=pulumi.ResourceOptions(provider=provider),
    )
