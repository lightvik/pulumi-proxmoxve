from pathlib import Path

import pulumi
import pulumi_proxmoxve as proxmox

from loader import load_inventory
from download import build_download_file

INV_PATH = Path("/workspace/inventory.yaml")
inv = load_inventory(INV_PATH)

provider = proxmox.Provider(
    "proxmox",
    endpoint=inv.provider.endpoint,
    insecure=inv.provider.insecure,
    api_token=inv.provider.api_token,
)

# ── Downloads (ISO / templates) ───────────────────────────────────────────────
# Если в inventory.yaml заданы downloads — скачиваем файлы через Proxmox API
# вместо ручного scp. Создаём template VM только после скачивания.
download_resources = [build_download_file(dl, provider) for dl in inv.downloads]

tmpl = inv.template

template_vm = proxmox.VmLegacy(
    "template-vm",
    node_name=inv.defaults.node,
    vm_id=tmpl.vmid,
    name="",
    description="Base template VM — managed by Pulumi",
    tags=["pulumi", "template"],
    bios=inv.defaults.bios,
    cpu=proxmox.VmLegacyCpuArgs(
        cores=inv.defaults.cpu.cores,
        type=inv.defaults.cpu.type,
    ),
    memory=proxmox.VmLegacyMemoryArgs(
        dedicated=inv.defaults.memory.dedicated,
    ),
    agent=proxmox.VmLegacyAgentArgs(
        enabled=inv.defaults.agent.enabled,
        trim=inv.defaults.agent.trim,
        type=inv.defaults.agent.type,
    ),
    disks=[
        proxmox.VmLegacyDiskArgs(
            interface="scsi0",
            size=d.size,
            datastore_id=d.datastore,
            discard="on",
        )
        for d in inv.defaults.disks
    ],
    cdrom=proxmox.VmLegacyCdromArgs(
        file_id=f"{tmpl.iso_datastore}:iso/{tmpl.iso_file}",
        interface="ide2",
    ),
    network_devices=[
        proxmox.VmLegacyNetworkDeviceArgs(
            bridge=list(inv.network.zones.values())[0].bridge,
            model="virtio",
        )
    ],
    on_boot=False,
    stop_on_destroy=True,
    started=False,
    opts=pulumi.ResourceOptions(
        provider=provider,
        depends_on=download_resources,
    ),
)

pulumi.export("template_vm_id", template_vm.vm_id)
pulumi.export("template_node", template_vm.node_name)
