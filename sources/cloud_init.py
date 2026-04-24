import pulumi
import pulumi_proxmoxve as proxmox

from models import Inventory


def build_cloud_init_file(
    inv: Inventory,
    provider: proxmox.Provider,
    public_key: pulumi.Output,
    resource_name: str = "cloud-init-user-data",
) -> proxmox.FileLegacy:
    node = inv.defaults.node
    datastore = inv.defaults.disks[0].datastore if inv.defaults.disks else "local"

    content = public_key.apply(
        lambda key: "\n".join([
            "#cloud-config",
            f"hostname: ${{HOSTNAME}}",
            f"fqdn: ${{HOSTNAME}}.{inv.network.domain}",
            "manage_etc_hosts: true",
            "users:",
            "  - name: ansible",
            "    groups: wheel",
            "    sudo: ALL=(ALL) NOPASSWD:ALL",
            "    shell: /bin/bash",
            "    ssh_authorized_keys:",
            f"      - {key}",
            "package_update: true",
            "packages:",
            "  - qemu-guest-agent",
            "runcmd:",
            "  - systemctl enable --now qemu-guest-agent",
        ])
    )

    return proxmox.FileLegacy(
        resource_name,
        node_name=node,
        datastore_id=datastore,
        content_type="snippets",
        source_raw=proxmox.FileLegacySourceRawArgs(
            data=content,
            file_name="cloud-init-user-data.yaml",
        ),
        opts=pulumi.ResourceOptions(provider=provider),
    )
