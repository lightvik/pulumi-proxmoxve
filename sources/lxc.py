import pulumi
import pulumi_proxmoxve as proxmox

from models import LxcSpec


def build_container(
    spec: LxcSpec,
    provider: proxmox.Provider,
    depends_on: list | None = None,
) -> proxmox.ContainerLegacy:
    network_interfaces = [
        proxmox.ContainerLegacyNetworkInterfaceArgs(
            name=net.name or f"eth{i}",
            bridge=net.bridge,
            enabled=net.enabled,
            firewall=net.firewall,
            mac_address=net.mac_address,
            mtu=net.mtu,
            rate_limit=net.rate_limit,
            vlan_id=net.vlan_id,
        )
        for i, net in enumerate(spec.networks)
    ]

    init = spec.initialization
    initialization_args: dict = {
        "hostname": init.hostname if init and init.hostname else spec.name
    }
    if init:
        if init.dns:
            initialization_args["dns"] = proxmox.ContainerLegacyInitializationDnsArgs(
                servers=init.dns.servers,
                domain=init.dns.domain,
            )
        if init.ip_configs:
            initialization_args["ip_configs"] = [
                proxmox.ContainerLegacyInitializationIpConfigArgs(
                    ipv4=proxmox.ContainerLegacyInitializationIpConfigIpv4Args(
                        address=c.ipv4.address,
                        gateway=c.ipv4.gateway,
                    )
                    if c.ipv4
                    else None,
                    ipv6=proxmox.ContainerLegacyInitializationIpConfigIpv6Args(
                        address=c.ipv6.address,
                        gateway=c.ipv6.gateway,
                    )
                    if c.ipv6
                    else None,
                )
                for c in init.ip_configs
            ]
        if init.user_account:
            initialization_args["user_account"] = (
                proxmox.ContainerLegacyInitializationUserAccountArgs(
                    username=init.user_account.username,
                    password=init.user_account.password,
                    keys=init.user_account.keys,
                )
            )
    initialization = proxmox.ContainerLegacyInitializationArgs(**initialization_args)

    ct_args: dict = {
        "node_name": spec.node,
        "vm_id": spec.vmid,
        "description": spec.description or "",
        "tags": spec.tags or ["pulumi"],
        "cpu": proxmox.ContainerLegacyCpuArgs(
            cores=spec.cpu.cores,
            architecture=spec.cpu.architecture,
            units=spec.cpu.units,
        ),
        "memory": proxmox.ContainerLegacyMemoryArgs(
            dedicated=spec.memory.dedicated,
            swap=spec.memory.swap,
        ),
        "disk": proxmox.ContainerLegacyDiskArgs(
            datastore_id=spec.disk.datastore,
            size=spec.disk.size,
            acl=spec.disk.acl,
            quota=spec.disk.quota,
            replicate=spec.disk.replicate,
            mount_options=spec.disk.mount_options,
        ),
        "network_interfaces": network_interfaces,
        "initialization": initialization,
        "opts": pulumi.ResourceOptions(
            provider=provider,
            depends_on=depends_on or [],
            ignore_changes=["started"] if spec.started == "keep" else None,
        ),
    }

    if spec.operating_system:
        ct_args["operating_system"] = proxmox.ContainerLegacyOperatingSystemArgs(
            template_file_id=spec.operating_system.template_file_id,
            type=spec.operating_system.type,
        )

    if spec.clone:
        ct_args["clone"] = proxmox.ContainerLegacyCloneArgs(
            vm_id=spec.clone.vm_id,
            datastore_id=spec.clone.datastore_id,
            node_name=spec.clone.node_name,
        )

    if spec.mount_points:
        ct_args["mount_points"] = [
            proxmox.ContainerLegacyMountPointArgs(
                path=mp.path,
                volume=mp.volume,
                acl=mp.acl,
                backup=mp.backup,
                mount_options=mp.mount_options,
                quota=mp.quota,
                read_only=mp.read_only,
                replicate=mp.replicate,
                shared=mp.shared,
                size=mp.size,
            )
            for mp in spec.mount_points
        ]

    if spec.features:
        ct_args["features"] = proxmox.ContainerLegacyFeaturesArgs(
            fuse=spec.features.fuse,
            keyctl=spec.features.keyctl,
            mounts=spec.features.mounts,
            nesting=spec.features.nesting,
        )

    if spec.unprivileged is not None:
        ct_args["unprivileged"] = spec.unprivileged
    if spec.start_on_boot is not None:
        ct_args["start_on_boot"] = spec.start_on_boot
    if spec.startup:
        ct_args["startup"] = proxmox.ContainerLegacyStartupArgs(
            order=spec.startup.order,
            up_delay=spec.startup.up_delay,
            down_delay=spec.startup.down_delay,
        )
    if spec.pool_id:
        ct_args["pool_id"] = spec.pool_id
    if spec.protection is not None:
        ct_args["protection"] = spec.protection
    if spec.started is not None and spec.started != "keep":
        ct_args["started"] = spec.started
    if spec.template is not None:
        ct_args["template"] = spec.template
    if spec.hook_script_file_id:
        ct_args["hook_script_file_id"] = spec.hook_script_file_id
    if spec.timeout_clone:
        ct_args["timeout_clone"] = spec.timeout_clone
    if spec.timeout_create:
        ct_args["timeout_create"] = spec.timeout_create
    if spec.timeout_delete:
        ct_args["timeout_delete"] = spec.timeout_delete
    if spec.timeout_start:
        ct_args["timeout_start"] = spec.timeout_start
    if spec.timeout_update:
        ct_args["timeout_update"] = spec.timeout_update

    return proxmox.ContainerLegacy(spec.name, **ct_args)
