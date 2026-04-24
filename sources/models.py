from __future__ import annotations

import ipaddress
from typing import Optional

from pydantic import BaseModel, model_validator


# ============================================================================
# PROVIDER & NETWORK
# ============================================================================


class Provider(BaseModel):
    endpoint: str
    insecure: bool = False
    api_token: Optional[str] = None


class Zone(BaseModel):
    bridge: str
    cidr: str
    gateway: str

    def ip_for_host(self, host: int) -> str:
        network = ipaddress.ip_network(self.cidr, strict=False)
        return str(network.network_address + host)


class Network(BaseModel):
    domain: str
    dns_servers: list[str]
    zones: dict[str, Zone]


# ============================================================================
# CPU CONFIGURATION
# ============================================================================


class CpuSpec(BaseModel):
    cores: int = 2
    type: str = "host"
    sockets: Optional[int] = None
    affinity: Optional[str] = None
    architecture: Optional[str] = None
    flags: Optional[str] = None
    hotplugged: Optional[int] = None
    limit: Optional[int] = None
    numa: Optional[bool] = None
    units: Optional[str] = None


# ============================================================================
# MEMORY CONFIGURATION
# ============================================================================


class MemorySpec(BaseModel):
    dedicated: int = 2048
    floating: Optional[int] = None
    hugepages: Optional[bool] = None
    keep_hugepages: Optional[bool] = None
    shared: Optional[int] = None


# ============================================================================
# DISK CONFIGURATION
# ============================================================================


class DiskSpec(BaseModel):
    size: int
    datastore: str
    aio: Optional[str] = None
    backup: Optional[bool] = None
    cache: Optional[str] = None
    discard: Optional[str] = None
    file_format: Optional[str] = None
    file_id: Optional[str] = None
    import_from: Optional[str] = None
    iothread: Optional[bool] = None
    path_in_datastore: Optional[str] = None
    replicate: Optional[bool] = None
    serial: Optional[str] = None
    speed: Optional[int] = None
    ssd: Optional[bool] = None


# ============================================================================
# AGENT CONFIGURATION
# ============================================================================


class AgentSpec(BaseModel):
    enabled: bool = True
    trim: bool = True
    type: str = "virtio"
    timeout: Optional[int] = None
    wait_for_ip: Optional[bool] = None


# ============================================================================
# NETWORK DEVICE CONFIGURATION
# ============================================================================


class NetworkDeviceSpec(BaseModel):
    zone: str
    host: int
    enabled: Optional[bool] = None
    disconnected: Optional[bool] = None
    firewall: Optional[bool] = None
    mac_address: Optional[str] = None
    mtu: Optional[int] = None
    queues: Optional[int] = None
    rate_limit: Optional[int] = None
    trunks: Optional[list[int]] = None
    vlan_id: Optional[int] = None


# ============================================================================
# CDROM CONFIGURATION
# ============================================================================


class CdromSpec(BaseModel):
    file_id: Optional[str] = None
    interface: Optional[str] = None
    enabled: Optional[bool] = None


# ============================================================================
# CLONE CONFIGURATION
# ============================================================================


class CloneSpec(BaseModel):
    vm_id: Optional[int] = None   # None → берётся из template стека
    node_name: Optional[str] = None
    datastore_id: Optional[str] = None
    full: bool = True
    retries: Optional[int] = None


# ============================================================================
# STARTUP/SHUTDOWN BEHAVIOR
# ============================================================================


class StartupSpec(BaseModel):
    order: Optional[int] = None
    up_delay: Optional[int] = None
    down_delay: Optional[int] = None


# ============================================================================
# NUMA CONFIGURATION
# ============================================================================


class NumaSpec(BaseModel):
    cpus: str
    memory: int
    device: Optional[str] = None
    hostnodes: Optional[str] = None
    policy: Optional[str] = None


# ============================================================================
# TPM STATE
# ============================================================================


class TpmStateSpec(BaseModel):
    version: Optional[str] = None
    datastore_id: Optional[str] = None


# ============================================================================
# EFI DISK (для OVMF BIOS)
# ============================================================================


class EfiDiskSpec(BaseModel):
    datastore_id: str
    file_format: Optional[str] = None
    pre_enrolled_keys: Optional[bool] = None
    type: Optional[str] = None


# ============================================================================
# VGA CONFIGURATION
# ============================================================================


class VgaSpec(BaseModel):
    type: Optional[str] = None
    memory: Optional[int] = None
    clipboard: Optional[str] = None


# ============================================================================
# WATCHDOG
# ============================================================================


class WatchdogSpec(BaseModel):
    model: Optional[str] = None
    action: Optional[str] = None
    enabled: Optional[bool] = None


# ============================================================================
# SMBIOS (системная информация)
# ============================================================================


class SmbiosSpec(BaseModel):
    manufacturer: Optional[str] = None
    product: Optional[str] = None
    serial: Optional[str] = None
    uuid: Optional[str] = None
    sku: Optional[str] = None
    family: Optional[str] = None
    version: Optional[str] = None


# ============================================================================
# RANDOM NUMBER GENERATOR
# ============================================================================


class RngSpec(BaseModel):
    source: str
    max_bytes: Optional[int] = None
    period: Optional[int] = None


# ============================================================================
# USB DEVICE
# ============================================================================


class UsbSpec(BaseModel):
    host: Optional[str] = None
    mapping: Optional[str] = None
    usb3: Optional[bool] = None


# ============================================================================
# SERIAL DEVICE
# ============================================================================


class SerialDeviceSpec(BaseModel):
    device: str


# ============================================================================
# HOST PCI DEVICE
# ============================================================================


class HostpciSpec(BaseModel):
    device: str
    id: Optional[str] = None
    mapping: Optional[str] = None
    mdev: Optional[str] = None
    pcie: Optional[bool] = None
    rom_file: Optional[str] = None
    rombar: Optional[bool] = None
    xvga: Optional[bool] = None


# ============================================================================
# AUDIO DEVICE
# ============================================================================


class AudioDeviceSpec(BaseModel):
    driver: str
    device: Optional[str] = None
    enabled: Optional[bool] = None


# ============================================================================
# AMD SEV (Secure Encrypted Virtualization)
# ============================================================================


class AmdSevSpec(BaseModel):
    type: str
    allow_smt: Optional[bool] = None
    kernel_hashes: Optional[bool] = None
    no_debug: Optional[bool] = None
    no_key_sharing: Optional[bool] = None


# ============================================================================
# VIRTIOFS (Shared memory filesystem)
# ============================================================================


class VirtiofSpec(BaseModel):
    mapping: str
    cache: Optional[str] = None
    direct_io: Optional[bool] = None
    expose_acl: Optional[bool] = None
    expose_xattr: Optional[bool] = None


# ============================================================================
# OPERATING SYSTEM
# ============================================================================


class OperatingSystemSpec(BaseModel):
    type: str


# ============================================================================
# INITIALIZATION / CLOUD-INIT
# ============================================================================


class InitializationDnsSpec(BaseModel):
    servers: list[str]
    domain: Optional[str] = None


class InitializationIpConfigIpv4Spec(BaseModel):
    address: str
    gateway: Optional[str] = None


class InitializationIpConfigIpv6Spec(BaseModel):
    address: str
    gateway: Optional[str] = None


class InitializationIpConfigSpec(BaseModel):
    ipv4: Optional[InitializationIpConfigIpv4Spec] = None
    ipv6: Optional[InitializationIpConfigIpv6Spec] = None


class InitializationUserAccountSpec(BaseModel):
    username: str
    password: Optional[str] = None
    keys: Optional[list[str]] = None
    groups: Optional[list[str]] = None


class InitializationSpec(BaseModel):
    type: Optional[str] = None
    datastore_id: Optional[str] = None
    interface: Optional[str] = None
    file_format: Optional[str] = None
    dns: Optional[InitializationDnsSpec] = None
    ip_configs: Optional[list[InitializationIpConfigSpec]] = None
    user_account: Optional[InitializationUserAccountSpec] = None
    user_data_file_id: Optional[str] = None
    vendor_data_file_id: Optional[str] = None
    meta_data_file_id: Optional[str] = None
    network_data_file_id: Optional[str] = None


# ============================================================================
# POOL
# ============================================================================


class PoolSpec(BaseModel):
    id: str
    comment: Optional[str] = None


# ============================================================================
# HIGH AVAILABILITY — GROUP
# ============================================================================


class HaGroupNodeSpec(BaseModel):
    node: str
    priority: Optional[int] = None


class HaGroupSpec(BaseModel):
    name: str
    comment: Optional[str] = None
    nodes: list[HaGroupNodeSpec] = []
    restricted: Optional[bool] = None
    no_failback: Optional[bool] = None


# ============================================================================
# HIGH AVAILABILITY — PER-VM
# ============================================================================


class HaSpec(BaseModel):
    enabled: bool = True
    group: Optional[str] = None
    state: str = "started"       # started | stopped | disabled
    max_restart: Optional[int] = None
    max_relocate: Optional[int] = None
    comment: Optional[str] = None


# ============================================================================
# HIGH AVAILABILITY — RULE (fencing)
# ============================================================================


class HaRuleSpec(BaseModel):
    id: str
    comment: Optional[str] = None


# ============================================================================
# DOWNLOAD FILE (ISO / vztmpl / etc.)
# ============================================================================


class DownloadFileSpec(BaseModel):
    name: str
    node: str
    datastore: str
    url: str
    filename: str
    content_type: str = "iso"   # iso | vztmpl | snippets
    checksum: Optional[str] = None
    checksum_algorithm: Optional[str] = None
    overwrite: Optional[bool] = None
    verify: Optional[bool] = None
    decompression_algorithm: Optional[str] = None


# ============================================================================
# SDN — Software Defined Networking
# ============================================================================


class SdnZoneSpec(BaseModel):
    name: str
    type: str                    # simple | qinq | vxlan | evpn
    comment: Optional[str] = None
    bridge: Optional[str] = None
    mtu: Optional[int] = None
    nodes: Optional[list[str]] = None


class SdnVnetSpec(BaseModel):
    name: str
    zone: str
    comment: Optional[str] = None
    tag: Optional[int] = None
    vlan_aware: Optional[bool] = None


class SdnSubnetSpec(BaseModel):
    cidr: str
    vnet: str
    gateway: Optional[str] = None
    snat: Optional[bool] = None


class SdnConfig(BaseModel):
    zones: list[SdnZoneSpec] = []
    vnets: list[SdnVnetSpec] = []
    subnets: list[SdnSubnetSpec] = []


# ============================================================================
# DEFAULTS
# ============================================================================


class Defaults(BaseModel):
    node: str
    cpu: CpuSpec = CpuSpec()
    memory: MemorySpec = MemorySpec()
    disks: list[DiskSpec] = []
    bios: str = "seabios"
    agent: AgentSpec = AgentSpec()
    acpi: Optional[bool] = None
    boot_orders: Optional[list[str]] = None
    cdrom: Optional[CdromSpec] = None
    delete_unreferenced_disks_on_destroy: Optional[bool] = None
    efi_disk: Optional[EfiDiskSpec] = None
    hook_script_file_id: Optional[str] = None
    hostpcis: Optional[list[HostpciSpec]] = None
    hotplug: Optional[str] = None
    keyboard_layout: Optional[str] = None
    kvm_arguments: Optional[str] = None
    machine: Optional[str] = None
    migrate: Optional[bool] = None
    on_boot: Optional[bool] = None
    operating_system: Optional[OperatingSystemSpec] = None
    pool_id: Optional[str] = None
    protection: Optional[bool] = None
    purge_on_destroy: Optional[bool] = None
    reboot: Optional[bool] = None
    reboot_after_update: Optional[bool] = None
    rngs: Optional[list[RngSpec]] = None
    scsi_hardware: Optional[str] = None
    serial_devices: Optional[list[SerialDeviceSpec]] = None
    smbios: Optional[SmbiosSpec] = None
    startup: Optional[StartupSpec] = None
    stop_on_destroy: Optional[bool] = None
    tablet_device: Optional[bool] = None
    tags: Optional[list[str]] = None
    template: Optional[bool] = None
    timeout_clone: Optional[int] = None
    timeout_create: Optional[int] = None
    timeout_migrate: Optional[int] = None
    timeout_move_disk: Optional[int] = None
    timeout_reboot: Optional[int] = None
    timeout_shutdown_vm: Optional[int] = None
    timeout_start_vm: Optional[int] = None
    timeout_stop_vm: Optional[int] = None
    tpm_state: Optional[TpmStateSpec] = None
    usbs: Optional[list[UsbSpec]] = None
    vga: Optional[VgaSpec] = None
    virtiofs: Optional[list[VirtiofSpec]] = None
    watchdog: Optional[WatchdogSpec] = None
    audio_device: Optional[AudioDeviceSpec] = None
    amd_sev: Optional[AmdSevSpec] = None
    numas: Optional[list[NumaSpec]] = None
    started: Optional[bool] = None


# ============================================================================
# TEMPLATE SPECIFICATION
# ============================================================================


class TemplateSpec(BaseModel):
    vmid: int
    iso_datastore: str
    iso_file: str


# ============================================================================
# VM NETWORK SPECIFICATION
# ============================================================================


class VMNetwork(NetworkDeviceSpec):
    pass


# ============================================================================
# VM SPECIFICATION
# ============================================================================


class VMSpec(BaseModel):
    name: str
    vmid: int
    networks: list[VMNetwork]
    cpu: Optional[CpuSpec] = None
    memory: Optional[MemorySpec] = None
    disks: Optional[list[DiskSpec]] = None
    acpi: Optional[bool] = None
    agent: Optional[AgentSpec] = None
    amd_sev: Optional[AmdSevSpec] = None
    audio_device: Optional[AudioDeviceSpec] = None
    boot_orders: Optional[list[str]] = None
    cdrom: Optional[CdromSpec] = None
    delete_unreferenced_disks_on_destroy: Optional[bool] = None
    efi_disk: Optional[EfiDiskSpec] = None
    hook_script_file_id: Optional[str] = None
    hostpcis: Optional[list[HostpciSpec]] = None
    hotplug: Optional[str] = None
    keyboard_layout: Optional[str] = None
    kvm_arguments: Optional[str] = None
    machine: Optional[str] = None
    migrate: Optional[bool] = None
    on_boot: Optional[bool] = None
    operating_system: Optional[OperatingSystemSpec] = None
    pool_id: Optional[str] = None
    protection: Optional[bool] = None
    purge_on_destroy: Optional[bool] = None
    reboot: Optional[bool] = None
    reboot_after_update: Optional[bool] = None
    rngs: Optional[list[RngSpec]] = None
    scsi_hardware: Optional[str] = None
    serial_devices: Optional[list[SerialDeviceSpec]] = None
    smbios: Optional[SmbiosSpec] = None
    startup: Optional[StartupSpec] = None
    stop_on_destroy: Optional[bool] = None
    tablet_device: Optional[bool] = None
    tags: Optional[list[str]] = None
    template: Optional[bool] = None
    timeout_clone: Optional[int] = None
    timeout_create: Optional[int] = None
    timeout_migrate: Optional[int] = None
    timeout_move_disk: Optional[int] = None
    timeout_reboot: Optional[int] = None
    timeout_shutdown_vm: Optional[int] = None
    timeout_start_vm: Optional[int] = None
    timeout_stop_vm: Optional[int] = None
    tpm_state: Optional[TpmStateSpec] = None
    usbs: Optional[list[UsbSpec]] = None
    vga: Optional[VgaSpec] = None
    virtiofs: Optional[list[VirtiofSpec]] = None
    watchdog: Optional[WatchdogSpec] = None
    numas: Optional[list[NumaSpec]] = None
    started: Optional[bool] = None
    bios: Optional[str] = None
    initialization: Optional[InitializationSpec] = None
    ha: Optional[HaSpec] = None
    clone: Optional[CloneSpec] = None

    def merged(self, defaults: Defaults) -> MergedVMSpec:
        return MergedVMSpec(
            name=self.name,
            vmid=self.vmid,
            networks=self.networks,
            node=defaults.node,
            cpu=self.cpu or defaults.cpu,
            memory=self.memory or defaults.memory,
            disks=self.disks if self.disks is not None else defaults.disks,
            bios=self.bios or defaults.bios,
            agent=self.agent or defaults.agent,
            acpi=self.acpi if self.acpi is not None else defaults.acpi,
            agent_amd_sev=self.amd_sev or defaults.amd_sev,
            audio_device=self.audio_device or defaults.audio_device,
            boot_orders=self.boot_orders or defaults.boot_orders,
            cdrom=self.cdrom or defaults.cdrom,
            delete_unreferenced_disks_on_destroy=self.delete_unreferenced_disks_on_destroy if self.delete_unreferenced_disks_on_destroy is not None else defaults.delete_unreferenced_disks_on_destroy,
            efi_disk=self.efi_disk or defaults.efi_disk,
            hook_script_file_id=self.hook_script_file_id or defaults.hook_script_file_id,
            hostpcis=self.hostpcis or defaults.hostpcis,
            hotplug=self.hotplug or defaults.hotplug,
            keyboard_layout=self.keyboard_layout or defaults.keyboard_layout,
            kvm_arguments=self.kvm_arguments or defaults.kvm_arguments,
            machine=self.machine or defaults.machine,
            migrate=self.migrate if self.migrate is not None else defaults.migrate,
            on_boot=self.on_boot if self.on_boot is not None else defaults.on_boot,
            operating_system=self.operating_system or defaults.operating_system,
            pool_id=self.pool_id or defaults.pool_id,
            protection=self.protection if self.protection is not None else defaults.protection,
            purge_on_destroy=self.purge_on_destroy if self.purge_on_destroy is not None else defaults.purge_on_destroy,
            reboot=self.reboot if self.reboot is not None else defaults.reboot,
            reboot_after_update=self.reboot_after_update if self.reboot_after_update is not None else defaults.reboot_after_update,
            rngs=self.rngs or defaults.rngs,
            scsi_hardware=self.scsi_hardware or defaults.scsi_hardware,
            serial_devices=self.serial_devices or defaults.serial_devices,
            smbios=self.smbios or defaults.smbios,
            startup=self.startup or defaults.startup,
            stop_on_destroy=self.stop_on_destroy if self.stop_on_destroy is not None else defaults.stop_on_destroy,
            tablet_device=self.tablet_device if self.tablet_device is not None else defaults.tablet_device,
            tags=self.tags or defaults.tags,
            template=self.template if self.template is not None else defaults.template,
            timeout_clone=self.timeout_clone or defaults.timeout_clone,
            timeout_create=self.timeout_create or defaults.timeout_create,
            timeout_migrate=self.timeout_migrate or defaults.timeout_migrate,
            timeout_move_disk=self.timeout_move_disk or defaults.timeout_move_disk,
            timeout_reboot=self.timeout_reboot or defaults.timeout_reboot,
            timeout_shutdown_vm=self.timeout_shutdown_vm or defaults.timeout_shutdown_vm,
            timeout_start_vm=self.timeout_start_vm or defaults.timeout_start_vm,
            timeout_stop_vm=self.timeout_stop_vm or defaults.timeout_stop_vm,
            tpm_state=self.tpm_state or defaults.tpm_state,
            usbs=self.usbs or defaults.usbs,
            vga=self.vga or defaults.vga,
            virtiofs=self.virtiofs or defaults.virtiofs,
            watchdog=self.watchdog or defaults.watchdog,
            numas=self.numas or defaults.numas,
            started=self.started if self.started is not None else defaults.started,
            initialization=self.initialization,
            ha=self.ha,
            clone=self.clone,
        )


# ============================================================================
# MERGED VM SPECIFICATION (после применения defaults)
# ============================================================================


class MergedVMSpec(BaseModel):
    name: str
    vmid: int
    networks: list[VMNetwork]
    node: str
    cpu: CpuSpec
    memory: MemorySpec
    disks: list[DiskSpec]
    bios: str
    agent: AgentSpec
    acpi: Optional[bool] = None
    agent_amd_sev: Optional[AmdSevSpec] = None
    audio_device: Optional[AudioDeviceSpec] = None
    boot_orders: Optional[list[str]] = None
    cdrom: Optional[CdromSpec] = None
    delete_unreferenced_disks_on_destroy: Optional[bool] = None
    efi_disk: Optional[EfiDiskSpec] = None
    hook_script_file_id: Optional[str] = None
    hostpcis: Optional[list[HostpciSpec]] = None
    hotplug: Optional[str] = None
    keyboard_layout: Optional[str] = None
    kvm_arguments: Optional[str] = None
    machine: Optional[str] = None
    migrate: Optional[bool] = None
    on_boot: Optional[bool] = None
    operating_system: Optional[OperatingSystemSpec] = None
    pool_id: Optional[str] = None
    protection: Optional[bool] = None
    purge_on_destroy: Optional[bool] = None
    reboot: Optional[bool] = None
    reboot_after_update: Optional[bool] = None
    rngs: Optional[list[RngSpec]] = None
    scsi_hardware: Optional[str] = None
    serial_devices: Optional[list[SerialDeviceSpec]] = None
    smbios: Optional[SmbiosSpec] = None
    startup: Optional[StartupSpec] = None
    stop_on_destroy: Optional[bool] = None
    tablet_device: Optional[bool] = None
    tags: Optional[list[str]] = None
    template: Optional[bool] = None
    timeout_clone: Optional[int] = None
    timeout_create: Optional[int] = None
    timeout_migrate: Optional[int] = None
    timeout_move_disk: Optional[int] = None
    timeout_reboot: Optional[int] = None
    timeout_shutdown_vm: Optional[int] = None
    timeout_start_vm: Optional[int] = None
    timeout_stop_vm: Optional[int] = None
    tpm_state: Optional[TpmStateSpec] = None
    usbs: Optional[list[UsbSpec]] = None
    vga: Optional[VgaSpec] = None
    virtiofs: Optional[list[VirtiofSpec]] = None
    watchdog: Optional[WatchdogSpec] = None
    numas: Optional[list[NumaSpec]] = None
    started: Optional[bool] = None
    initialization: Optional[InitializationSpec] = None
    ha: Optional[HaSpec] = None
    clone: Optional[CloneSpec] = None


# ============================================================================
# INVENTORY (главная модель)
# ============================================================================


class Inventory(BaseModel):
    provider: Provider
    network: Network
    defaults: Defaults
    template: TemplateSpec
    vms: list[VMSpec]
    pools: list[PoolSpec] = []
    ha_groups: list[HaGroupSpec] = []
    downloads: list[DownloadFileSpec] = []
    sdn: Optional[SdnConfig] = None

    @model_validator(mode="after")
    def validate_vm_zones(self) -> Inventory:
        for vm in self.vms:
            for net in vm.networks:
                if net.zone not in self.network.zones:
                    raise ValueError(
                        f"VM '{vm.name}': zone '{net.zone}' not found in network.zones"
                    )
        ha_group_names = {g.name for g in self.ha_groups}
        for vm in self.vms:
            if vm.ha and vm.ha.group and vm.ha.group not in ha_group_names:
                raise ValueError(
                    f"VM '{vm.name}': ha.group '{vm.ha.group}' not found in ha_groups"
                )
        return self
