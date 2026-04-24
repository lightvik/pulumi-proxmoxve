import ipaddress

import pulumi
import pulumi_proxmoxve as proxmox

from models import Inventory, MergedVMSpec


def build_vm(
    spec: MergedVMSpec,
    inv: Inventory,
    provider: proxmox.Provider,
    template_id: int,
    cloud_init_file_id: pulumi.Input[str] | None = None,
) -> proxmox.VmLegacy:
    network_devices = []
    ip_configs = []
    for net in spec.networks:
        zone = inv.network.zones[net.zone]
        ip = _ip_for_host(zone.cidr, net.host)
        prefix = _prefix_len(zone.cidr)
        network_devices.append(
            proxmox.VmLegacyNetworkDeviceArgs(
                bridge=zone.bridge,
                model="virtio",
                enabled=net.enabled,
                disconnected=net.disconnected,
                firewall=net.firewall,
                mac_address=net.mac_address,
                mtu=net.mtu,
                queues=net.queues,
                rate_limit=net.rate_limit,
                trunks=net.trunks,
                vlan_id=net.vlan_id,
            )
        )
        ip_configs.append(
            proxmox.VmLegacyInitializationIpConfigArgs(
                ipv4=proxmox.VmLegacyInitializationIpConfigIpv4Args(
                    address=f"{ip}/{prefix}",
                    gateway=zone.gateway,
                )
            )
        )

    disks = [
        proxmox.VmLegacyDiskArgs(
            interface=f"scsi{i}",
            size=d.size,
            datastore_id=d.datastore,
            discard=d.discard or "on",
            aio=d.aio,
            backup=d.backup,
            cache=d.cache,
            file_format=d.file_format,
            file_id=d.file_id,
            import_from=d.import_from,
            iothread=d.iothread,
            path_in_datastore=d.path_in_datastore,
            replicate=d.replicate,
            serial=d.serial,
            speed=d.speed,
            ssd=d.ssd,
        )
        for i, d in enumerate(spec.disks)
    ]

    initialization_args = {
        "datastore_id": spec.disks[0].datastore if spec.disks else "local",
    }
    if spec.initialization:
        if spec.initialization.type:
            initialization_args["type"] = spec.initialization.type
        if spec.initialization.interface:
            initialization_args["interface"] = spec.initialization.interface
        if spec.initialization.file_format:
            initialization_args["file_format"] = spec.initialization.file_format
        if spec.initialization.dns or inv.network.dns_servers:
            initialization_args["dns"] = proxmox.VmLegacyInitializationDnsArgs(
                servers=spec.initialization.dns.servers if spec.initialization.dns else inv.network.dns_servers,
                domain=spec.initialization.dns.domain if spec.initialization.dns else inv.network.domain,
            )
        if spec.initialization.ip_configs or ip_configs:
            initialization_args["ip_configs"] = spec.initialization.ip_configs or ip_configs
        if cloud_init_file_id:
            initialization_args["user_data_file_id"] = cloud_init_file_id
        if spec.initialization.user_data_file_id:
            initialization_args["user_data_file_id"] = spec.initialization.user_data_file_id
        if spec.initialization.vendor_data_file_id:
            initialization_args["vendor_data_file_id"] = spec.initialization.vendor_data_file_id
        if spec.initialization.meta_data_file_id:
            initialization_args["meta_data_file_id"] = spec.initialization.meta_data_file_id
        if spec.initialization.network_data_file_id:
            initialization_args["network_data_file_id"] = spec.initialization.network_data_file_id
    elif cloud_init_file_id or ip_configs:
        initialization_args["dns"] = proxmox.VmLegacyInitializationDnsArgs(
            servers=inv.network.dns_servers,
            domain=inv.network.domain,
        )
        if ip_configs:
            initialization_args["ip_configs"] = ip_configs
        if cloud_init_file_id:
            initialization_args["user_data_file_id"] = cloud_init_file_id

    initialization = proxmox.VmLegacyInitializationArgs(**initialization_args)

    vm_args = {
        "node_name": spec.node,
        "vm_id": spec.vmid,
        "name": spec.name,
        "description": f"Managed by Pulumi — {spec.name}.{inv.network.domain}",
        "tags": spec.tags or ["pulumi"],
        "bios": spec.bios,
        "cpu": proxmox.VmLegacyCpuArgs(
            cores=spec.cpu.cores,
            type=spec.cpu.type,
            sockets=spec.cpu.sockets,
            affinity=spec.cpu.affinity,
            architecture=spec.cpu.architecture,
            flags=spec.cpu.flags,
            hotplugged=spec.cpu.hotplugged,
            limit=spec.cpu.limit,
            numa=spec.cpu.numa,
            units=spec.cpu.units,
        ),
        "memory": proxmox.VmLegacyMemoryArgs(
            dedicated=spec.memory.dedicated,
            floating=spec.memory.floating,
            hugepages=spec.memory.hugepages,
            keep_hugepages=spec.memory.keep_hugepages,
            shared=spec.memory.shared,
        ),
        "agent": proxmox.VmLegacyAgentArgs(
            enabled=spec.agent.enabled,
            trim=spec.agent.trim,
            type=spec.agent.type,
            timeout=spec.agent.timeout,
            wait_for_ip=spec.agent.wait_for_ip,
        ),
        "network_devices": network_devices,
        "disks": disks,
        "initialization": initialization,
        "clone": proxmox.VmLegacyCloneArgs(
            vm_id=spec.clone.vm_id if (spec.clone and spec.clone.vm_id is not None) else template_id,
            node_name=spec.clone.node_name if spec.clone else spec.node,
            full=spec.clone.full if spec.clone else True,
            datastore_id=spec.clone.datastore_id if spec.clone else None,
            retries=spec.clone.retries if spec.clone else None,
        ),
        "opts": pulumi.ResourceOptions(provider=provider),
    }

    if spec.acpi is not None:
        vm_args["acpi"] = spec.acpi
    if spec.boot_orders:
        vm_args["boot_orders"] = spec.boot_orders
    if spec.cdrom:
        vm_args["cdrom"] = proxmox.VmLegacyCdromArgs(
            file_id=spec.cdrom.file_id,
            interface=spec.cdrom.interface,
            enabled=spec.cdrom.enabled,
        )
    if spec.delete_unreferenced_disks_on_destroy is not None:
        vm_args["delete_unreferenced_disks_on_destroy"] = spec.delete_unreferenced_disks_on_destroy
    if spec.efi_disk:
        vm_args["efi_disk"] = proxmox.VmLegacyEfiDiskArgs(
            datastore_id=spec.efi_disk.datastore_id,
            file_format=spec.efi_disk.file_format,
            pre_enrolled_keys=spec.efi_disk.pre_enrolled_keys,
            type=spec.efi_disk.type,
        )
    if spec.hook_script_file_id:
        vm_args["hook_script_file_id"] = spec.hook_script_file_id
    if spec.hostpcis:
        vm_args["hostpcis"] = [
            proxmox.VmLegacyHostpciArgs(
                device=h.device,
                id=h.id,
                mapping=h.mapping,
                mdev=h.mdev,
                pcie=h.pcie,
                rom_file=h.rom_file,
                rombar=h.rombar,
                xvga=h.xvga,
            )
            for h in spec.hostpcis
        ]
    if spec.hotplug:
        vm_args["hotplug"] = spec.hotplug
    if spec.keyboard_layout:
        vm_args["keyboard_layout"] = spec.keyboard_layout
    if spec.kvm_arguments:
        vm_args["kvm_arguments"] = spec.kvm_arguments
    if spec.machine:
        vm_args["machine"] = spec.machine
    if spec.migrate is not None:
        vm_args["migrate"] = spec.migrate
    if spec.on_boot is not None:
        vm_args["on_boot"] = spec.on_boot
    if spec.operating_system:
        vm_args["operating_system"] = proxmox.VmLegacyOperatingSystemArgs(
            type=spec.operating_system.type
        )
    if spec.pool_id:
        vm_args["pool_id"] = spec.pool_id
    if spec.protection is not None:
        vm_args["protection"] = spec.protection
    if spec.purge_on_destroy is not None:
        vm_args["purge_on_destroy"] = spec.purge_on_destroy
    if spec.reboot is not None:
        vm_args["reboot"] = spec.reboot
    if spec.reboot_after_update is not None:
        vm_args["reboot_after_update"] = spec.reboot_after_update
    if spec.rngs:
        vm_args["rngs"] = [
            proxmox.VmLegacyRngArgs(
                source=r.source,
                max_bytes=r.max_bytes,
                period=r.period,
            )
            for r in spec.rngs
        ]
    if spec.scsi_hardware:
        vm_args["scsi_hardware"] = spec.scsi_hardware
    if spec.serial_devices:
        vm_args["serial_devices"] = [
            proxmox.VmLegacySerialDeviceArgs(device=s.device)
            for s in spec.serial_devices
        ]
    if spec.smbios:
        vm_args["smbios"] = proxmox.VmLegacySmbiosArgs(
            family=spec.smbios.family,
            manufacturer=spec.smbios.manufacturer,
            product=spec.smbios.product,
            serial=spec.smbios.serial,
            sku=spec.smbios.sku,
            uuid=spec.smbios.uuid,
            version=spec.smbios.version,
        )
    if spec.startup:
        vm_args["startup"] = proxmox.VmLegacyStartupArgs(
            order=spec.startup.order,
            up_delay=spec.startup.up_delay,
            down_delay=spec.startup.down_delay,
        )
    if spec.stop_on_destroy is not None:
        vm_args["stop_on_destroy"] = spec.stop_on_destroy
    if spec.tablet_device is not None:
        vm_args["tablet_device"] = spec.tablet_device
    if spec.template is not None:
        vm_args["template"] = spec.template
    if spec.timeout_clone:
        vm_args["timeout_clone"] = spec.timeout_clone
    if spec.timeout_create:
        vm_args["timeout_create"] = spec.timeout_create
    if spec.timeout_migrate:
        vm_args["timeout_migrate"] = spec.timeout_migrate
    if spec.timeout_move_disk:
        vm_args["timeout_move_disk"] = spec.timeout_move_disk
    if spec.timeout_reboot:
        vm_args["timeout_reboot"] = spec.timeout_reboot
    if spec.timeout_shutdown_vm:
        vm_args["timeout_shutdown_vm"] = spec.timeout_shutdown_vm
    if spec.timeout_start_vm:
        vm_args["timeout_start_vm"] = spec.timeout_start_vm
    if spec.timeout_stop_vm:
        vm_args["timeout_stop_vm"] = spec.timeout_stop_vm
    if spec.tpm_state:
        vm_args["tpm_state"] = proxmox.VmLegacyTpmStateArgs(
            datastore_id=spec.tpm_state.datastore_id,
            version=spec.tpm_state.version,
        )
    if spec.usbs:
        vm_args["usbs"] = [
            proxmox.VmLegacyUsbArgs(
                host=u.host,
                mapping=u.mapping,
                usb3=u.usb3,
            )
            for u in spec.usbs
        ]
    if spec.vga:
        vm_args["vga"] = proxmox.VmLegacyVgaArgs(
            clipboard=spec.vga.clipboard,
            memory=spec.vga.memory,
            type=spec.vga.type,
        )
    if spec.virtiofs:
        vm_args["virtiofs"] = [
            proxmox.VmLegacyVirtiofArgs(
                mapping=v.mapping,
                cache=v.cache,
                direct_io=v.direct_io,
                expose_acl=v.expose_acl,
                expose_xattr=v.expose_xattr,
            )
            for v in spec.virtiofs
        ]
    if spec.watchdog:
        vm_args["watchdog"] = proxmox.VmLegacyWatchdogArgs(
            action=spec.watchdog.action,
            enabled=spec.watchdog.enabled,
            model=spec.watchdog.model,
        )
    if spec.agent_amd_sev:
        vm_args["amd_sev"] = proxmox.VmLegacyAmdSevArgs(
            type=spec.agent_amd_sev.type,
            allow_smt=spec.agent_amd_sev.allow_smt,
            kernel_hashes=spec.agent_amd_sev.kernel_hashes,
            no_debug=spec.agent_amd_sev.no_debug,
            no_key_sharing=spec.agent_amd_sev.no_key_sharing,
        )
    if spec.audio_device:
        vm_args["audio_device"] = proxmox.VmLegacyAudioDeviceArgs(
            device=spec.audio_device.device,
            driver=spec.audio_device.driver,
            enabled=spec.audio_device.enabled,
        )
    if spec.numas:
        vm_args["numas"] = [
            proxmox.VmLegacyNumaArgs(
                cpus=n.cpus,
                device=n.device,
                hostnodes=n.hostnodes,
                memory=n.memory,
                policy=n.policy,
            )
            for n in spec.numas
        ]
    if spec.started is not None:
        vm_args["started"] = spec.started

    return proxmox.VmLegacy(spec.name, **vm_args)


def _ip_for_host(cidr: str, host: int) -> str:
    network = ipaddress.ip_network(cidr, strict=False)
    return str(network.network_address + host)


def _prefix_len(cidr: str) -> int:
    return ipaddress.ip_network(cidr, strict=False).prefixlen
