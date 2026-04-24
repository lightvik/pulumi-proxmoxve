from pathlib import Path

import pulumi
import pulumi_proxmoxve as proxmox

from loader import load_inventory
from ssh_key import build_ssh_key
from cloud_init import build_cloud_init_file
from vm import build_vm
from pool import build_pool
from ha import build_ha_group, build_ha_resource
from sdn import build_sdn_zone, build_sdn_vnet, build_sdn_subnet

INV_PATH = Path("/workspace/inventory.yaml")
inv = load_inventory(INV_PATH)

provider = proxmox.Provider(
    "proxmox",
    endpoint=inv.provider.endpoint,
    insecure=inv.provider.insecure,
    api_token=inv.provider.api_token,
)

# ── Pools ────────────────────────────────────────────────────────────────────
pools = {spec.id: build_pool(spec, provider) for spec in inv.pools}

# ── HA groups ────────────────────────────────────────────────────────────────
ha_groups = {spec.name: build_ha_group(spec, provider) for spec in inv.ha_groups}

# ── SDN ──────────────────────────────────────────────────────────────────────
sdn_zones: dict = {}
sdn_vnets: dict = {}
if inv.sdn:
    for zone_spec in inv.sdn.zones:
        sdn_zones[zone_spec.name] = build_sdn_zone(zone_spec, provider)
    for vnet_spec in inv.sdn.vnets:
        zone = sdn_zones[vnet_spec.zone]
        sdn_vnets[vnet_spec.name] = build_sdn_vnet(vnet_spec, zone, provider)
    for subnet_spec in inv.sdn.subnets:
        vnet = sdn_vnets[subnet_spec.vnet]
        build_sdn_subnet(subnet_spec, vnet, provider)

# ── SSH key + cloud-init ─────────────────────────────────────────────────────
ssh_key = build_ssh_key()
cloud_init = build_cloud_init_file(inv, provider, ssh_key.public_key_openssh)

# ── VMs ──────────────────────────────────────────────────────────────────────
vms = {}
for spec in inv.vms:
    merged_spec = spec.merged(inv.defaults)
    vm = build_vm(
        spec=merged_spec,
        inv=inv,
        provider=provider,
        template_id=inv.template.vmid,
        cloud_init_file_id=cloud_init.id,
    )
    vms[spec.name] = vm

    if merged_spec.ha and merged_spec.ha.enabled:
        build_ha_resource(merged_spec, vm, provider)

# ── Outputs ──────────────────────────────────────────────────────────────────
pulumi.export("ssh_private_key", pulumi.Output.secret(ssh_key.private_key_openssh))
pulumi.export("ssh_public_key", ssh_key.public_key_openssh)
pulumi.export(
    "vm_ips",
    pulumi.Output.all(**{
        name: vm.initialization.apply(
            lambda init: init.ip_configs[0].ipv4.address if init and init.ip_configs else "unknown"
        )
        for name, vm in vms.items()
    }),
)
