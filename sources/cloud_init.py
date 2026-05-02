import pulumi
import pulumi_proxmoxve as proxmox


def build_cloud_init_file(
    node: str,
    datastore: str,
    provider: proxmox.Provider,
    public_key: pulumi.Output,
    resource_name: str = "cloud-init-user-data",
) -> proxmox.FileLegacy:
    content = public_key.apply(
        lambda key: "\n".join([
            "#cloud-config",
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
