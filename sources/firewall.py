import pulumi
import pulumi_proxmoxve as proxmox

from models import (
    FirewallConfig,
    ClusterFirewallSpec,
    FwSecurityGroupSpec,
    NodeFirewallSpec,
    FwAliasSpec,
    FwIpsetSpec,
    FwOptionsSpec,
    FwRulesSpec,
    FwRuleSpec,
)


def _build_rules(rules: list[FwRuleSpec]) -> list:
    result = []
    for r in rules:
        args: dict = {}
        if r.type is not None:
            args["type"] = r.type
        if r.action is not None:
            args["action"] = r.action
        if r.enabled is not None:
            args["enabled"] = r.enabled
        if r.comment is not None:
            args["comment"] = r.comment
        if r.source is not None:
            args["source"] = r.source
        if r.dest is not None:
            args["dest"] = r.dest
        if r.proto is not None:
            args["proto"] = r.proto
        if r.dport is not None:
            args["dport"] = r.dport
        if r.sport is not None:
            args["sport"] = r.sport
        if r.iface is not None:
            args["iface"] = r.iface
        if r.log is not None:
            args["log"] = r.log
        if r.macro is not None:
            args["macro"] = r.macro
        if r.security_group is not None:
            args["security_group"] = r.security_group
        if r.pos is not None:
            args["pos"] = r.pos
        result.append(args)
    return result


def build_cluster_firewall(
    spec: ClusterFirewallSpec,
    provider: proxmox.Provider,
) -> proxmox.cluster.FirewallLegacy:
    args: dict = {}
    if spec.enabled is not None:
        args["enabled"] = spec.enabled
    if spec.ebtables is not None:
        args["ebtables"] = spec.ebtables
    if spec.forward_policy is not None:
        args["forward_policy"] = spec.forward_policy
    if spec.input_policy is not None:
        args["input_policy"] = spec.input_policy
    if spec.output_policy is not None:
        args["output_policy"] = spec.output_policy
    if spec.log_ratelimit is not None:
        lr = spec.log_ratelimit
        args["log_ratelimit"] = proxmox.cluster.FirewallLegacyLogRatelimitArgs(
            enabled=lr.enabled,
            burst=lr.burst,
            rate=lr.rate,
        )

    return proxmox.cluster.FirewallLegacy(
        "cluster-firewall",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_fw_security_group(
    spec: FwSecurityGroupSpec,
    provider: proxmox.Provider,
) -> proxmox.cluster.firewall.security.GroupLegacy:
    args: dict = {}
    if spec.comment is not None:
        args["comment"] = spec.comment
    if spec.node_name is not None:
        args["node_name"] = spec.node_name
    if spec.vm_id is not None:
        args["vm_id"] = spec.vm_id
    if spec.container_id is not None:
        args["container_id"] = spec.container_id
    if spec.rules:
        args["rules"] = [
            proxmox.cluster.firewall.security.GroupLegacyRuleArgs(**r)
            for r in _build_rules(spec.rules)
        ]

    return proxmox.cluster.firewall.security.GroupLegacy(
        f"fw-security-group-{spec.name}",
        name=spec.name,
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_node_firewall(
    spec: NodeFirewallSpec,
    provider: proxmox.Provider,
) -> proxmox.node.Firewall:
    args: dict = {"node_name": spec.node}
    if spec.enabled is not None:
        args["enabled"] = spec.enabled
    if spec.nftables is not None:
        args["nftables"] = spec.nftables
    if spec.ndp is not None:
        args["ndp"] = spec.ndp
    if spec.nosmurfs is not None:
        args["nosmurfs"] = spec.nosmurfs
    if spec.log_level_in is not None:
        args["log_level_in"] = spec.log_level_in
    if spec.log_level_out is not None:
        args["log_level_out"] = spec.log_level_out
    if spec.log_level_forward is not None:
        args["log_level_forward"] = spec.log_level_forward
    if spec.smurf_log_level is not None:
        args["smurf_log_level"] = spec.smurf_log_level
    if spec.tcp_flags_log_level is not None:
        args["tcp_flags_log_level"] = spec.tcp_flags_log_level
    if spec.nf_conntrack_max is not None:
        args["nf_conntrack_max"] = spec.nf_conntrack_max
    if spec.nf_conntrack_tcp_timeout_established is not None:
        args["nf_conntrack_tcp_timeout_established"] = (
            spec.nf_conntrack_tcp_timeout_established
        )

    return proxmox.node.Firewall(
        f"node-firewall-{spec.node}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_fw_alias(
    spec: FwAliasSpec,
    provider: proxmox.Provider,
) -> proxmox.firewall.AliasLegacy:
    args: dict = {}
    if spec.cidr is not None:
        args["cidr"] = spec.cidr
    if spec.comment is not None:
        args["comment"] = spec.comment
    if spec.node_name is not None:
        args["node_name"] = spec.node_name
    if spec.vm_id is not None:
        args["vm_id"] = spec.vm_id
    if spec.container_id is not None:
        args["container_id"] = spec.container_id

    return proxmox.firewall.AliasLegacy(
        f"fw-alias-{spec.name}",
        name=spec.name,
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_fw_ipset(
    spec: FwIpsetSpec,
    provider: proxmox.Provider,
) -> proxmox.firewall.IpsetLegacy:
    args: dict = {}
    if spec.comment is not None:
        args["comment"] = spec.comment
    if spec.node_name is not None:
        args["node_name"] = spec.node_name
    if spec.vm_id is not None:
        args["vm_id"] = spec.vm_id
    if spec.container_id is not None:
        args["container_id"] = spec.container_id
    if spec.cidrs:
        args["cidrs"] = [
            proxmox.firewall.IpsetLegacyCidrArgs(
                name=c.name,
                comment=c.comment,
                nomatch=c.nomatch,
            )
            for c in spec.cidrs
        ]

    return proxmox.firewall.IpsetLegacy(
        f"fw-ipset-{spec.name}",
        name=spec.name,
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_fw_options(
    spec: FwOptionsSpec,
    provider: proxmox.Provider,
) -> proxmox.firewall.OptionsLegacy:
    args: dict = {}
    if spec.node_name is not None:
        args["node_name"] = spec.node_name
    if spec.vm_id is not None:
        args["vm_id"] = spec.vm_id
    if spec.container_id is not None:
        args["container_id"] = spec.container_id
    if spec.enabled is not None:
        args["enabled"] = spec.enabled
    if spec.dhcp is not None:
        args["dhcp"] = spec.dhcp
    if spec.ipfilter is not None:
        args["ipfilter"] = spec.ipfilter
    if spec.macfilter is not None:
        args["macfilter"] = spec.macfilter
    if spec.ndp is not None:
        args["ndp"] = spec.ndp
    if spec.radv is not None:
        args["radv"] = spec.radv
    if spec.input_policy is not None:
        args["input_policy"] = spec.input_policy
    if spec.output_policy is not None:
        args["output_policy"] = spec.output_policy
    if spec.log_level_in is not None:
        args["log_level_in"] = spec.log_level_in
    if spec.log_level_out is not None:
        args["log_level_out"] = spec.log_level_out

    return proxmox.firewall.OptionsLegacy(
        f"fw-options-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_fw_rules(
    spec: FwRulesSpec,
    provider: proxmox.Provider,
) -> proxmox.firewall.RulesLegacy:
    args: dict = {}
    if spec.node_name is not None:
        args["node_name"] = spec.node_name
    if spec.vm_id is not None:
        args["vm_id"] = spec.vm_id
    if spec.container_id is not None:
        args["container_id"] = spec.container_id
    if spec.rules:
        args["rules"] = [
            proxmox.firewall.RulesLegacyRuleArgs(**r) for r in _build_rules(spec.rules)
        ]

    return proxmox.firewall.RulesLegacy(
        f"fw-rules-{spec.name}",
        **args,
        opts=pulumi.ResourceOptions(provider=provider),
    )


def build_firewall(cfg: FirewallConfig, provider: proxmox.Provider) -> None:
    if cfg.cluster is not None:
        build_cluster_firewall(cfg.cluster, provider)
    for spec in cfg.security_groups:
        build_fw_security_group(spec, provider)
    for spec in cfg.node_firewalls:
        build_node_firewall(spec, provider)
    for spec in cfg.aliases:
        build_fw_alias(spec, provider)
    for spec in cfg.ipsets:
        build_fw_ipset(spec, provider)
    for spec in cfg.options:
        build_fw_options(spec, provider)
    for spec in cfg.rules:
        build_fw_rules(spec, provider)
