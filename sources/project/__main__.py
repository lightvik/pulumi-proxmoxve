from pathlib import Path

import pulumi
import pulumi_proxmoxve as proxmox

from loader import load_inventory
from vm import build_vm
from lxc import build_container
from pool import build_pool
from ha import build_ha_group, build_ha_resource, build_ha_rule
from backup import build_backup_job
from replication import build_replication
from rbac import build_rbac
from firewall import build_firewall
from acme import build_acme
from cluster_misc import build_cluster_misc
from sdn import (
    build_sdn_zone,
    build_sdn_vnet,
    build_sdn_subnet,
    build_sdn_applier,
    build_sdn_fabric_openfabric,
    build_sdn_fabric_ospf,
    build_sdn_fabric_node_openfabric,
    build_sdn_fabric_node_ospf,
)
from download import build_download_file
from upload import build_upload_file
from cloned_vm import build_cloned_vm
from network import build_linux_bridge, build_linux_vlan
from node_config import build_dns, build_hosts, build_time
from storage import build_storages

INV_PATH = Path("/workspace/inventory.yaml")
inv = load_inventory(INV_PATH)

provider = proxmox.Provider(
    "proxmox",
    endpoint=inv.provider.endpoint,
    insecure=inv.provider.insecure,
    api_token=inv.provider.api_token,
)

# ── RBAC (roles / groups / users / tokens / ACLs / realms) ───────────────────
if inv.rbac:
    build_rbac(inv.rbac, provider)

# ── Firewall ──────────────────────────────────────────────────────────────────
if inv.firewall:
    build_firewall(inv.firewall, provider)

# ── ACME (DNS plugins / accounts / certificates) ──────────────────────────────
if inv.acme:
    build_acme(inv.acme, provider)

# ── Cluster misc (Options / HW mappings / Metrics / OCI / APT / Pool membership)
if inv.cluster_misc:
    build_cluster_misc(inv.cluster_misc, provider)

# ── Storages ─────────────────────────────────────────────────────────────────
if inv.storages:
    build_storages(inv.storages, provider)

# ── Network bridges & VLANs ──────────────────────────────────────────────────
for spec in inv.network_bridges:
    build_linux_bridge(spec, provider)

for spec in inv.network_vlans:
    build_linux_vlan(spec, provider)

# ── Node config (DNS / hosts / time) ─────────────────────────────────────────
for spec in inv.node_dns:
    build_dns(spec, provider)

for spec in inv.node_hosts:
    build_hosts(spec, provider)

for spec in inv.node_time:
    build_time(spec, provider)

# ── Downloads ────────────────────────────────────────────────────────────────
download_resources = [build_download_file(dl, provider) for dl in inv.downloads]

# ── Uploads (локальные файлы → Proxmox storage) ───────────────────────────────
upload_resources = [build_upload_file(ul, provider) for ul in inv.uploads]

# ── Pools ────────────────────────────────────────────────────────────────────
pools = {spec.id: build_pool(spec, provider) for spec in inv.pools}

# ── HA groups ────────────────────────────────────────────────────────────────
ha_groups = {spec.name: build_ha_group(spec, provider) for spec in inv.ha_groups}

# ── HA fencing rules ─────────────────────────────────────────────────────────
for spec in inv.ha_rules:
    build_ha_rule(spec, provider)

# ── Backup jobs ───────────────────────────────────────────────────────────────
for spec in inv.backups:
    build_backup_job(spec, provider)

# ── Replication ───────────────────────────────────────────────────────────────
for spec in inv.replications:
    build_replication(spec, provider)

# ── SDN ──────────────────────────────────────────────────────────────────────
sdn_zones: dict[str, pulumi.CustomResource] = {}
sdn_vnets: dict[str, pulumi.CustomResource] = {}
sdn_fabrics_openfabric: dict[str, pulumi.CustomResource] = {}
sdn_fabrics_ospf: dict[str, pulumi.CustomResource] = {}
if inv.sdn:
    for zone_spec in inv.sdn.zones:
        sdn_zones[zone_spec.name] = build_sdn_zone(zone_spec, provider)
    for vnet_spec in inv.sdn.vnets:
        zone_res = sdn_zones[vnet_spec.zone]
        sdn_vnets[vnet_spec.name] = build_sdn_vnet(vnet_spec, zone_res, provider)
    for subnet_spec in inv.sdn.subnets:
        vnet_res = sdn_vnets[subnet_spec.vnet]
        build_sdn_subnet(subnet_spec, vnet_res, provider)
    for spec in inv.sdn.fabric_openfabric:
        sdn_fabrics_openfabric[spec.name] = build_sdn_fabric_openfabric(spec, provider)
    for spec in inv.sdn.fabric_ospf:
        sdn_fabrics_ospf[spec.name] = build_sdn_fabric_ospf(spec, provider)
    for spec in inv.sdn.fabric_node_openfabric:
        fabric_res = sdn_fabrics_openfabric[spec.fabric_id]
        build_sdn_fabric_node_openfabric(spec, fabric_res, provider)
    for spec in inv.sdn.fabric_node_ospf:
        fabric_res = sdn_fabrics_ospf[spec.fabric_id]
        build_sdn_fabric_node_ospf(spec, fabric_res, provider)
    if inv.sdn.applier:
        build_sdn_applier(inv.sdn.applier, provider)

# ── VMs ──────────────────────────────────────────────────────────────────────
# Two-pass: templates first so clones can declare depends_on.
vm_resources: dict[str, proxmox.VmLegacy] = {}
template_by_vmid: dict[int, proxmox.VmLegacy] = {}

for spec in inv.vms:
    if spec.template:
        vm = build_vm(
            spec=spec,
            provider=provider,
            depends_on=(download_resources + upload_resources) or None,
        )
        vm_resources[spec.name] = vm
        template_by_vmid[spec.vmid] = vm

for spec in inv.vms:
    if spec.template:
        continue
    deps: list = upload_resources[:]
    if spec.clone and spec.clone.vm_id in template_by_vmid:
        deps.append(template_by_vmid[spec.clone.vm_id])
    vm = build_vm(
        spec=spec,
        provider=provider,
        depends_on=deps or None,
    )
    vm_resources[spec.name] = vm

    if spec.ha and spec.ha.enabled:
        build_ha_resource(spec, vm, provider)

# ── Cloned VMs (облегчённый ресурс) ──────────────────────────────────────────
for spec in inv.cloned_vms:
    build_cloned_vm(spec, provider)

# ── LXC Containers ───────────────────────────────────────────────────────────
container_resources: dict[str, proxmox.ContainerLegacy] = {}

for spec in inv.containers:
    ct = build_container(
        spec=spec,
        provider=provider,
    )
    container_resources[spec.name] = ct

# ── Outputs ──────────────────────────────────────────────────────────────────
template_vm_names = {s.name for s in inv.vms if s.template}
pulumi.export(
    "vm_ips",
    pulumi.Output.all(
        **{
            name: vm.initialization.apply(
                lambda init: (
                    init.ip_configs[0].ipv4.address
                    if init and init.ip_configs and init.ip_configs[0].ipv4
                    else "unknown"
                )
            )
            for name, vm in vm_resources.items()
            if name not in template_vm_names
        }
    ),
)
