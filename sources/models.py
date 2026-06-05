from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, model_validator


# ============================================================================
# PROVIDER
# ============================================================================


class ProviderSshSpec(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    private_key: Optional[str] = None
    agent: Optional[bool] = None


class Provider(BaseModel):
    endpoint: str
    insecure: bool = False
    api_token: Optional[str] = None
    ssh: Optional[ProviderSshSpec] = None


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


class DiskSpeedSpec(BaseModel):
    read: Optional[int] = None
    read_burstable: Optional[int] = None
    write: Optional[int] = None
    write_burstable: Optional[int] = None
    iops_read: Optional[int] = None
    iops_read_burstable: Optional[int] = None
    iops_write: Optional[int] = None
    iops_write_burstable: Optional[int] = None


class DiskSpec(BaseModel):
    size: int
    datastore: str  # maps to datastore_id in proxmox
    aio: Optional[str] = None
    backup: Optional[bool] = None
    cache: Optional[str] = None
    discard: Optional[str] = "on"  # default "on"; pass None to disable
    file_format: Optional[str] = None
    file_id: Optional[str] = None
    import_from: Optional[str] = None
    iothread: Optional[bool] = None
    path_in_datastore: Optional[str] = None
    replicate: Optional[bool] = None
    serial: Optional[str] = None
    speed: Optional[DiskSpeedSpec] = None
    ssd: Optional[bool] = None


# ============================================================================
# AGENT CONFIGURATION
# ============================================================================


class AgentWaitForIpSpec(BaseModel):
    ipv4: Optional[bool] = None
    ipv6: Optional[bool] = None


class AgentSpec(BaseModel):
    enabled: bool = True
    trim: bool = True
    type: str = "virtio"
    timeout: Optional[str] = "10s"
    wait_for_ip: Optional[AgentWaitForIpSpec] = None


# ============================================================================
# NETWORK DEVICE CONFIGURATION
# ============================================================================


class NetworkDeviceSpec(BaseModel):
    bridge: str
    model: str = "virtio"
    enabled: Optional[bool] = None
    disconnected: Optional[bool] = None
    firewall: Optional[bool] = None
    mac_address: Optional[str] = None
    mtu: Optional[int] = None
    queues: Optional[int] = None
    rate_limit: Optional[float] = None
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
# CLONE CONFIGURATION (VM)
# ============================================================================


class CloneSpec(BaseModel):
    vm_id: int
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


class InitializationSpec(BaseModel):
    type: Optional[str] = None
    interface: Optional[str] = None
    file_format: Optional[str] = None
    dns: Optional[InitializationDnsSpec] = None
    ip_configs: Optional[list[InitializationIpConfigSpec]] = None
    upgrade: Optional[bool] = None
    user_account: Optional[InitializationUserAccountSpec] = None
    user_data_file_id: Optional[str] = None
    vendor_data_file_id: Optional[str] = None
    meta_data_file_id: Optional[str] = None
    network_data_file_id: Optional[str] = None


class LxcInitializationSpec(BaseModel):
    hostname: Optional[str] = None
    dns: Optional[InitializationDnsSpec] = None
    ip_configs: Optional[list[InitializationIpConfigSpec]] = None
    user_account: Optional[InitializationUserAccountSpec] = None


# ============================================================================
# NETWORK — Linux bridges and VLANs on Proxmox nodes
# ============================================================================


class NetworkBridgeSpec(BaseModel):
    node: str
    name: str  # e.g. vmbr1
    address: Optional[str] = None  # IPv4/CIDR
    address6: Optional[str] = None  # IPv6/CIDR
    autostart: Optional[bool] = None
    comment: Optional[str] = None
    gateway: Optional[str] = None
    gateway6: Optional[str] = None
    mtu: Optional[int] = None
    ports: Optional[list[str]] = None
    timeout_reload: Optional[int] = None
    vlan_aware: Optional[bool] = None


class NetworkVlanSpec(BaseModel):
    node: str
    name: str  # e.g. ens18.10 or vlan_lab
    address: Optional[str] = None
    address6: Optional[str] = None
    autostart: Optional[bool] = None
    comment: Optional[str] = None
    gateway: Optional[str] = None
    gateway6: Optional[str] = None
    interface: Optional[str] = None  # raw device (required for custom name)
    mtu: Optional[int] = None
    timeout_reload: Optional[int] = None
    vlan: Optional[int] = None  # VLAN tag (required for custom name)


# ============================================================================
# NODE CONFIG — DNS, /etc/hosts, timezone
# ============================================================================


class NodeDnsSpec(BaseModel):
    node: str
    domain: Optional[str] = None
    servers: list[str]


class NodeHostsEntrySpec(BaseModel):
    address: str
    hostnames: list[str]


class NodeHostsSpec(BaseModel):
    node: str
    entries: list[NodeHostsEntrySpec]


class NodeTimeSpec(BaseModel):
    node: str
    time_zone: str


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
    state: str = "started"  # started | stopped | disabled
    max_restart: Optional[int] = None
    max_relocate: Optional[int] = None
    comment: Optional[str] = None


# ============================================================================
# HIGH AVAILABILITY — RULE (fencing)
# ============================================================================


class HaRuleSpec(BaseModel):
    name: str
    resource_id: Optional[str] = None
    affinity: Optional[str] = None  # "required" | "preferred"
    comment: Optional[str] = None
    disable: Optional[bool] = None
    nodes: Optional[dict[str, int]] = None  # {node_name: priority}
    resources: Optional[list[str]] = None  # ["vm:100", "ct:200"]
    rule: Optional[str] = None
    strict: Optional[bool] = None
    type: Optional[str] = None  # "lxc" | "qemu" | "service" | "storage"


# ============================================================================
# BACKUP JOB
# ============================================================================


class BackupJobFleecingSpec(BaseModel):
    enabled: Optional[bool] = None
    storage: Optional[str] = None


class BackupJobPerformanceSpec(BaseModel):
    max_workers: Optional[int] = None
    pbs_entries_max: Optional[int] = None


class BackupJobSpec(BaseModel):
    name: str
    resource_id: Optional[str] = None
    storage: Optional[str] = None
    schedule: Optional[str] = None
    all: Optional[bool] = None
    vmids: Optional[list[str]] = None
    pool: Optional[str] = None
    node: Optional[str] = None
    enabled: Optional[bool] = None
    mode: Optional[str] = None  # "snapshot" | "suspend" | "stop"
    compress: Optional[str] = None  # "0" | "1" | "gzip" | "lzo" | "zstd"
    mailnotification: Optional[str] = None  # "always" | "failure"
    mailtos: Optional[list[str]] = None
    notes_template: Optional[str] = None
    exclude_paths: Optional[list[str]] = None
    fleecing: Optional[BackupJobFleecingSpec] = None
    performance: Optional[BackupJobPerformanceSpec] = None
    prune_backups: Optional[dict[str, str]] = None
    bwlimit: Optional[int] = None
    ionice: Optional[int] = None
    lockwait: Optional[int] = None
    maxfiles: Optional[int] = None
    pigz: Optional[int] = None
    stopwait: Optional[int] = None
    zstd: Optional[int] = None
    pbs_change_detection_mode: Optional[str] = None
    protected: Optional[bool] = None
    remove: Optional[bool] = None
    repeat_missed: Optional[bool] = None
    script: Optional[str] = None
    starttime: Optional[str] = None
    stdexcludes: Optional[bool] = None
    tmpdir: Optional[str] = None


# ============================================================================
# REPLICATION
# ============================================================================


class ReplicationSpec(BaseModel):
    name: str
    resource_id: Optional[str] = None
    target: Optional[str] = None
    schedule: Optional[str] = None
    comment: Optional[str] = None
    disable: Optional[bool] = None
    rate: Optional[float] = None
    type: Optional[str] = None  # "local"


# ============================================================================
# FIREWALL
# ============================================================================


class FwLogRatelimitSpec(BaseModel):
    enabled: Optional[bool] = None
    burst: Optional[int] = None
    rate: Optional[str] = None  # e.g. "1/second"


class FwRuleSpec(BaseModel):
    type: Optional[str] = None  # "in" | "out" | "group"
    action: Optional[str] = None  # "ACCEPT" | "DROP" | "REJECT"
    enabled: Optional[bool] = None
    comment: Optional[str] = None
    source: Optional[str] = None
    dest: Optional[str] = None
    proto: Optional[str] = None
    dport: Optional[str] = None
    sport: Optional[str] = None
    iface: Optional[str] = None
    log: Optional[str] = None
    macro: Optional[str] = None
    security_group: Optional[str] = None
    pos: Optional[int] = None


class FwIpsetCidrSpec(BaseModel):
    name: str  # CIDR string, e.g. "10.0.0.0/8"
    comment: Optional[str] = None
    nomatch: Optional[bool] = None


class ClusterFirewallSpec(BaseModel):
    enabled: Optional[bool] = None
    ebtables: Optional[bool] = None
    forward_policy: Optional[str] = None  # "ACCEPT" | "DROP" | "REJECT"
    input_policy: Optional[str] = None
    output_policy: Optional[str] = None
    log_ratelimit: Optional[FwLogRatelimitSpec] = None


class FwSecurityGroupSpec(BaseModel):
    name: str
    comment: Optional[str] = None
    node_name: Optional[str] = None
    vm_id: Optional[int] = None
    container_id: Optional[int] = None
    rules: list[FwRuleSpec] = []


class NodeFirewallSpec(BaseModel):
    node: str
    enabled: Optional[bool] = None
    nftables: Optional[bool] = None
    ndp: Optional[bool] = None
    nosmurfs: Optional[bool] = None
    log_level_in: Optional[str] = None
    log_level_out: Optional[str] = None
    log_level_forward: Optional[str] = None
    smurf_log_level: Optional[str] = None
    tcp_flags_log_level: Optional[str] = None
    nf_conntrack_max: Optional[int] = None
    nf_conntrack_tcp_timeout_established: Optional[int] = None


class FwAliasSpec(BaseModel):
    name: str
    cidr: Optional[str] = None
    comment: Optional[str] = None
    node_name: Optional[str] = None
    vm_id: Optional[int] = None
    container_id: Optional[int] = None


class FwIpsetSpec(BaseModel):
    name: str
    comment: Optional[str] = None
    node_name: Optional[str] = None
    vm_id: Optional[int] = None
    container_id: Optional[int] = None
    cidrs: list[FwIpsetCidrSpec] = []


class FwOptionsSpec(BaseModel):
    name: str
    node_name: Optional[str] = None
    vm_id: Optional[int] = None
    container_id: Optional[int] = None
    enabled: Optional[bool] = None
    dhcp: Optional[bool] = None
    ipfilter: Optional[bool] = None
    macfilter: Optional[bool] = None
    ndp: Optional[bool] = None
    radv: Optional[bool] = None
    input_policy: Optional[str] = None
    output_policy: Optional[str] = None
    log_level_in: Optional[str] = None
    log_level_out: Optional[str] = None


class FwRulesSpec(BaseModel):
    name: str
    node_name: Optional[str] = None
    vm_id: Optional[int] = None
    container_id: Optional[int] = None
    rules: list[FwRuleSpec] = []


class FirewallConfig(BaseModel):
    cluster: Optional[ClusterFirewallSpec] = None
    security_groups: list[FwSecurityGroupSpec] = []
    node_firewalls: list[NodeFirewallSpec] = []
    aliases: list[FwAliasSpec] = []
    ipsets: list[FwIpsetSpec] = []
    options: list[FwOptionsSpec] = []
    rules: list[FwRulesSpec] = []


# ============================================================================
# RBAC — Roles, Groups, Users, Tokens, ACLs, Realms
# ============================================================================


class RoleSpec(BaseModel):
    name: str
    role_id: Optional[str] = None
    privileges: Optional[list[str]] = None


class GroupAclEntrySpec(BaseModel):
    path: str
    role_id: str
    propagate: Optional[bool] = None


class GroupSpec(BaseModel):
    name: str
    group_id: Optional[str] = None
    comment: Optional[str] = None
    acls: list[GroupAclEntrySpec] = []


class UserAclEntrySpec(BaseModel):
    path: str
    role_id: str
    propagate: Optional[bool] = None


class UserSpec(BaseModel):
    name: str
    user_id: Optional[str] = None
    comment: Optional[str] = None
    email: Optional[str] = None
    enabled: Optional[bool] = None
    expiration_date: Optional[str] = None
    first_name: Optional[str] = None
    groups: Optional[list[str]] = None
    keys: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    acls: list[UserAclEntrySpec] = []


class UserTokenSpec(BaseModel):
    name: str
    user_id: Optional[str] = None
    token_name: Optional[str] = None
    comment: Optional[str] = None
    expiration_date: Optional[str] = None
    privileges_separation: Optional[bool] = None


class AclSpec(BaseModel):
    name: str
    path: Optional[str] = None
    role_id: Optional[str] = None
    user_id: Optional[str] = None
    group_id: Optional[str] = None
    token_id: Optional[str] = None
    propagate: Optional[bool] = None


class RealmLdapSpec(BaseModel):
    name: str
    realm: Optional[str] = None
    server1: Optional[str] = None
    server2: Optional[str] = None
    port: Optional[int] = None
    base_dn: Optional[str] = None
    bind_dn: Optional[str] = None
    bind_password: Optional[str] = None
    user_attr: Optional[str] = None
    user_classes: Optional[str] = None
    group_dn: Optional[str] = None
    group_classes: Optional[str] = None
    group_filter: Optional[str] = None
    group_name_attr: Optional[str] = None
    filter: Optional[str] = None
    sync_attributes: Optional[str] = None
    sync_defaults_options: Optional[str] = None
    mode: Optional[str] = None  # "ldap" | "ldaps" | "ldap+starttls"
    ssl_version: Optional[str] = None
    ca_path: Optional[str] = None
    cert_path: Optional[str] = None
    cert_key_path: Optional[str] = None
    case_sensitive: Optional[bool] = None
    comment: Optional[str] = None
    default: Optional[bool] = None
    secure: Optional[bool] = None
    verify: Optional[bool] = None


class RealmOpenIdSpec(BaseModel):
    name: str
    realm: Optional[str] = None
    issuer_url: Optional[str] = None
    client_id: Optional[str] = None
    client_key: Optional[str] = None
    username_claim: Optional[str] = None
    scopes: Optional[str] = None
    acr_values: Optional[str] = None
    prompt: Optional[str] = None
    groups_claim: Optional[str] = None
    autocreate: Optional[bool] = None
    comment: Optional[str] = None
    default: Optional[bool] = None
    groups_autocreate: Optional[bool] = None
    groups_overwrite: Optional[bool] = None
    query_userinfo: Optional[bool] = None


class RealmSyncSpec(BaseModel):
    name: str
    realm: Optional[str] = None
    scope: Optional[str] = None  # "users" | "groups" | "both"
    dry_run: Optional[bool] = None
    enable_new: Optional[bool] = None
    full: Optional[bool] = None
    purge: Optional[bool] = None
    remove_vanished: Optional[str] = None


class RbacConfig(BaseModel):
    roles: list[RoleSpec] = []
    groups: list[GroupSpec] = []
    users: list[UserSpec] = []
    user_tokens: list[UserTokenSpec] = []
    acls: list[AclSpec] = []
    realm_ldap: list[RealmLdapSpec] = []
    realm_openid: list[RealmOpenIdSpec] = []
    realm_sync: list[RealmSyncSpec] = []


# ============================================================================
# STORAGE BACKENDS
# ============================================================================


class StorageNfsSpec(BaseModel):
    resource_id: str
    server: str
    export: str
    contents: Optional[list[str]] = (
        None  # ["images", "iso", "vztmpl", "backup", "snippets", "rootdir"]
    )
    nodes: Optional[list[str]] = None
    disable: Optional[bool] = None
    backups: Optional[bool] = None
    options: Optional[str] = None
    preallocation: Optional[str] = None
    snapshot_as_volume_chain: Optional[bool] = None


class StorageCifsSpec(BaseModel):
    resource_id: str
    server: str
    share: str
    username: str
    password: str
    contents: Optional[list[str]] = None
    nodes: Optional[list[str]] = None
    disable: Optional[bool] = None
    backups: Optional[bool] = None
    domain: Optional[str] = None
    subdirectory: Optional[str] = None
    preallocation: Optional[str] = None
    snapshot_as_volume_chain: Optional[bool] = None


class StorageLvmSpec(BaseModel):
    resource_id: str
    volume_group: str
    contents: Optional[list[str]] = None
    nodes: Optional[list[str]] = None
    disable: Optional[bool] = None
    shared: Optional[bool] = None
    wipe_removed_volumes: Optional[bool] = None


class StorageLvmThinSpec(BaseModel):
    resource_id: str
    volume_group: str
    thin_pool: str
    contents: Optional[list[str]] = None
    nodes: Optional[list[str]] = None
    disable: Optional[bool] = None


class StorageZfspoolSpec(BaseModel):
    resource_id: str
    zfs_pool: str
    blocksize: Optional[str] = None
    contents: Optional[list[str]] = None
    nodes: Optional[list[str]] = None
    disable: Optional[bool] = None
    thin_provision: Optional[bool] = None


class StoragePbsSpec(BaseModel):
    resource_id: str
    server: str
    datastore: str
    username: str
    password: str
    contents: Optional[list[str]] = None
    nodes: Optional[list[str]] = None
    disable: Optional[bool] = None
    backups: Optional[bool] = None
    encryption_key: Optional[str] = None
    fingerprint: Optional[str] = None
    generate_encryption_key: Optional[bool] = None
    namespace: Optional[str] = None


class StorageDirectorySpec(BaseModel):
    resource_id: str
    path: str
    contents: Optional[list[str]] = None
    nodes: Optional[list[str]] = None
    disable: Optional[bool] = None
    backups: Optional[bool] = None
    preallocation: Optional[str] = None
    shared: Optional[bool] = None


class StorageConfig(BaseModel):
    nfs: list[StorageNfsSpec] = []
    cifs: list[StorageCifsSpec] = []
    lvm: list[StorageLvmSpec] = []
    lvmthin: list[StorageLvmThinSpec] = []
    zfspool: list[StorageZfspoolSpec] = []
    pbs: list[StoragePbsSpec] = []
    dir: list[StorageDirectorySpec] = []


# ============================================================================
# DOWNLOAD FILE (ISO / vztmpl / etc.)
# ============================================================================


class DownloadFileSpec(BaseModel):
    name: str
    node: str
    datastore: str
    url: str
    filename: str
    content_type: str = "iso"  # iso | vztmpl | snippets
    checksum: Optional[str] = None
    checksum_algorithm: Optional[str] = None
    overwrite: Optional[bool] = None
    verify: Optional[bool] = None
    decompression_algorithm: Optional[str] = None


# ============================================================================
# UPLOAD FILE (загрузка с локальной машины через API)
# ============================================================================


class UploadFileSourceSpec(BaseModel):
    path: str  # путь к локальному файлу или URL
    checksum: Optional[str] = None  # SHA256
    file_name: Optional[str] = None  # переопределить имя файла в хранилище
    insecure: Optional[bool] = None  # пропустить TLS-проверку для URL


class UploadFileSpec(BaseModel):
    name: str
    node: str
    datastore: str
    source_file: UploadFileSourceSpec
    content_type: Optional[str] = None  # iso | snippets | vztmpl
    file_mode: Optional[str] = None  # e.g. "0644"
    overwrite: Optional[bool] = None
    timeout_upload: Optional[int] = None  # секунды, по умолчанию 1800


# ============================================================================
# SDN — Software Defined Networking
# ============================================================================


class SdnZoneSpec(BaseModel):
    name: str
    type: str  # simple | qinq | vxlan | evpn
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


class SdnApplierSpec(BaseModel):
    on_create: Optional[bool] = None
    on_destroy: Optional[bool] = None
    legacy: bool = False


class SdnFabricOpenfabricSpec(BaseModel):
    name: str
    csnp_interval: Optional[int] = None
    hello_interval: Optional[int] = None
    ip6_prefix: Optional[str] = None
    ip_prefix: Optional[str] = None
    legacy: bool = False


class SdnFabricOspfSpec(BaseModel):
    name: str
    area: str
    ip_prefix: str
    legacy: bool = False


class SdnFabricNodeOpenfabricSpec(BaseModel):
    fabric_id: str
    node_id: str
    interface_names: list[str]
    ip: Optional[str] = None
    ip6: Optional[str] = None
    legacy: bool = False


class SdnFabricNodeOspfSpec(BaseModel):
    fabric_id: str
    node_id: str
    interface_names: list[str]
    ip: str
    legacy: bool = False


class SdnConfig(BaseModel):
    zones: list[SdnZoneSpec] = []
    vnets: list[SdnVnetSpec] = []
    subnets: list[SdnSubnetSpec] = []
    applier: Optional[SdnApplierSpec] = None
    fabric_openfabric: list[SdnFabricOpenfabricSpec] = []
    fabric_ospf: list[SdnFabricOspfSpec] = []
    fabric_node_openfabric: list[SdnFabricNodeOpenfabricSpec] = []
    fabric_node_ospf: list[SdnFabricNodeOspfSpec] = []


# ============================================================================
# LXC — CPU, MEMORY, DISK, NETWORK, FEATURES, CLONE
# ============================================================================


class LxcCpuSpec(BaseModel):
    cores: int = 1
    architecture: Optional[str] = None
    units: Optional[int] = None


class LxcMemorySpec(BaseModel):
    dedicated: int = 512
    swap: Optional[int] = None


class LxcDiskSpec(BaseModel):
    size: int = 4
    datastore: str = "local"  # maps to datastore_id in proxmox
    acl: Optional[bool] = None
    quota: Optional[bool] = None
    replicate: Optional[bool] = None
    mount_options: Optional[list[str]] = None


class LxcNetworkInterfaceSpec(BaseModel):
    bridge: str
    name: Optional[str] = None  # auto-assigned as eth{i} if None
    enabled: Optional[bool] = None
    firewall: Optional[bool] = None
    mac_address: Optional[str] = None
    mtu: Optional[int] = None
    rate_limit: Optional[float] = None  # MB/s
    vlan_id: Optional[int] = None


class LxcMountPointSpec(BaseModel):
    path: str
    volume: str
    acl: Optional[bool] = None
    backup: Optional[bool] = None
    mount_options: Optional[list[str]] = None
    quota: Optional[bool] = None
    read_only: Optional[bool] = None
    replicate: Optional[bool] = None
    shared: Optional[bool] = None
    size: Optional[str] = None  # e.g. "10G"


class LxcFeaturesSpec(BaseModel):
    fuse: Optional[bool] = None
    keyctl: Optional[bool] = None
    mounts: Optional[list[str]] = None  # ["cifs", "nfs"]
    nesting: Optional[bool] = None


class LxcCloneSpec(BaseModel):
    vm_id: int
    datastore_id: Optional[str] = None
    node_name: Optional[str] = None


class LxcOperatingSystemSpec(BaseModel):
    template_file_id: str
    type: Optional[str] = None  # ubuntu | debian | alpine | etc.


# ============================================================================
# VM SPECIFICATION
# ============================================================================


class VMSpec(BaseModel):
    name: str
    vmid: int
    node: str
    networks: list[NetworkDeviceSpec]
    cpu: CpuSpec = CpuSpec()
    memory: MemorySpec = MemorySpec()
    disks: list[DiskSpec] = []
    bios: str = "seabios"
    agent: AgentSpec = AgentSpec()
    acpi: Optional[bool] = None
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
    started: Optional[bool | Literal["keep"]] = None
    initialization: Optional[InitializationSpec] = None
    ha: Optional[HaSpec] = None
    clone: Optional[CloneSpec] = None


# ============================================================================
# CLONED VM (облегчённый ресурс cloned.Vm / cloned.VmLegacy)
# ============================================================================


class ClonedVmCloneSpec(BaseModel):
    source_vm_id: int
    bandwidth_limit: Optional[int] = None
    full: Optional[bool] = None
    pool_id: Optional[str] = None
    retries: Optional[int] = None
    snapshot_name: Optional[str] = None
    source_node_name: Optional[str] = None  # нода-источник шаблона
    target_datastore: Optional[str] = None
    target_format: Optional[str] = None  # raw | qcow2


class ClonedVmSpec(BaseModel):
    name: str
    node: str
    clone: ClonedVmCloneSpec
    description: Optional[str] = None
    tags: list[str] = []
    started: Optional[bool | Literal["keep"]] = None
    stop_on_destroy: Optional[bool] = None
    purge_on_destroy: Optional[bool] = None
    delete_unreferenced_disks_on_destroy: Optional[bool] = None
    legacy: bool = True  # True → cloned.VmLegacy, False → cloned.Vm


# ============================================================================
# LXC CONTAINER SPECIFICATION
# ============================================================================


class LxcSpec(BaseModel):
    name: str
    vmid: int
    node: str
    networks: list[LxcNetworkInterfaceSpec]
    cpu: LxcCpuSpec = LxcCpuSpec()
    memory: LxcMemorySpec = LxcMemorySpec()
    disk: LxcDiskSpec = LxcDiskSpec()
    initialization: Optional[LxcInitializationSpec] = None
    operating_system: Optional[LxcOperatingSystemSpec] = None
    mount_points: Optional[list[LxcMountPointSpec]] = None
    features: Optional[LxcFeaturesSpec] = None
    clone: Optional[LxcCloneSpec] = None
    unprivileged: Optional[bool] = None
    start_on_boot: Optional[bool] = None
    startup: Optional[StartupSpec] = None
    pool_id: Optional[str] = None
    protection: Optional[bool] = None
    started: Optional[bool | Literal["keep"]] = None
    tags: Optional[list[str]] = None
    template: Optional[bool] = None
    hook_script_file_id: Optional[str] = None
    timeout_clone: Optional[int] = None
    timeout_create: Optional[int] = None
    timeout_delete: Optional[int] = None
    timeout_start: Optional[int] = None
    timeout_update: Optional[int] = None


# ============================================================================
# ACME — DNS-плагины, аккаунты, сертификаты
# ============================================================================


class AcmeDnsPluginSpec(BaseModel):
    name: str  # Pulumi resource name (becomes plugin id)
    plugin: Optional[str] = None  # lego plugin name, e.g. "cloudflare"
    api: Optional[str] = None  # API type, e.g. "dns"
    data: Optional[dict[str, str]] = None  # plugin-specific key/value config
    disable: Optional[bool] = None
    validation_delay: Optional[int] = None  # seconds
    digest: Optional[str] = None


class AcmeAccountSpec(BaseModel):
    name: str  # account name in Proxmox
    contact: Optional[str] = None  # mailto:admin@example.com
    directory: Optional[str] = None  # CA directory URL (Let's Encrypt = default)
    eab_hmac_key: Optional[str] = None  # External Account Binding HMAC key
    eab_kid: Optional[str] = None  # External Account Binding key ID
    tos: Optional[str] = None  # Terms of Service URL


class AcmeCertDomainSpec(BaseModel):
    domain: str  # e.g. "pve.example.com"
    plugin: Optional[str] = None  # DNS plugin name (DNS-01) or omit for HTTP-01
    alias: Optional[str] = None  # alias domain for DNS validation


class AcmeCertificateSpec(BaseModel):
    name: str  # Pulumi resource name
    node_name: str
    account: Optional[str] = None  # ACME account name
    domains: list[AcmeCertDomainSpec] = []
    force: Optional[bool] = None
    legacy: bool = False  # True → acme.CertificateLegacy


class NodeCertificateSpec(BaseModel):
    name: str  # Pulumi resource name
    node_name: str
    certificate: Optional[str] = None  # PEM certificate
    certificate_chain: Optional[str] = None
    private_key: Optional[str] = None
    overwrite: Optional[bool] = None


class AcmeConfig(BaseModel):
    dns_plugins: list[AcmeDnsPluginSpec] = []
    accounts: list[AcmeAccountSpec] = []
    certificates: list[AcmeCertificateSpec] = []
    node_certificates: list[NodeCertificateSpec] = []


# ============================================================================
# CLUSTER MISC — Options, Hardware Mappings, Metrics, OCI, APT, Pool Membership
# ============================================================================


class ClusterOptionsNextIdSpec(BaseModel):
    lower: Optional[int] = None
    upper: Optional[int] = None


class ClusterOptionsNotifySpec(BaseModel):
    ha_fencing_mode: Optional[str] = None
    ha_fencing_target: Optional[str] = None
    package_updates: Optional[str] = None  # "auto" | "always" | "never"
    package_updates_target: Optional[str] = None
    replication: Optional[str] = None  # "always" | "never"
    replication_target: Optional[str] = None


class ClusterOptionsSpec(BaseModel):
    bandwidth_limit_clone: Optional[int] = None
    bandwidth_limit_default: Optional[int] = None
    bandwidth_limit_migration: Optional[int] = None
    bandwidth_limit_move: Optional[int] = None
    bandwidth_limit_restore: Optional[int] = None
    console: Optional[str] = None  # "applet" | "html5" | "vv" | "xtermjs"
    crs_ha: Optional[str] = None  # "static" | "basic"
    crs_ha_rebalance_on_start: Optional[bool] = None
    description: Optional[str] = None
    email_from: Optional[str] = None
    ha_shutdown_policy: Optional[str] = (
        None  # "freeze" | "failover" | "conditional" | "migrate"
    )
    http_proxy: Optional[str] = None
    keyboard: Optional[str] = None
    language: Optional[str] = None
    mac_prefix: Optional[str] = None
    max_workers: Optional[int] = None
    migration_cidr: Optional[str] = None
    migration_type: Optional[str] = None  # "secure" | "unsecure"
    next_id: Optional[ClusterOptionsNextIdSpec] = None
    notify: Optional[ClusterOptionsNotifySpec] = None


class HwPciMapSpec(BaseModel):
    id: str  # PCI device ID, e.g. "0000:01:00.0"
    node: str
    path: str
    comment: Optional[str] = None
    iommu_group: Optional[int] = None
    subsystem_id: Optional[str] = None


class HwMappingPciSpec(BaseModel):
    name: str
    comment: Optional[str] = None
    mediated_devices: Optional[bool] = None
    maps: list[HwPciMapSpec] = []
    legacy: bool = False  # True → PciLegacy, False → Pci


class HwUsbMapSpec(BaseModel):
    id: str  # USB device ID, e.g. "1234:5678"
    node: str
    comment: Optional[str] = None
    path: Optional[str] = None  # optional port path


class HwMappingUsbSpec(BaseModel):
    name: str
    comment: Optional[str] = None
    maps: list[HwUsbMapSpec] = []
    legacy: bool = False  # True → UsbLegacy, False → Usb


class HwDirMapSpec(BaseModel):
    node: str
    path: str  # POSIX-путь на ноде, например /mnt/data


class HwMappingDirSpec(BaseModel):
    name: str
    comment: Optional[str] = None
    maps: list[HwDirMapSpec] = []
    legacy: bool = False  # True → DirLegacy, False → Dir


class MetricsServerSpec(BaseModel):
    name: str
    disable: Optional[bool] = None
    graphite_path: Optional[str] = None
    graphite_proto: Optional[str] = None  # "udp" | "tcp"
    influx_api_path_prefix: Optional[str] = None
    influx_bucket: Optional[str] = None
    influx_db_proto: Optional[str] = None
    influx_max_body_size: Optional[int] = None
    influx_organization: Optional[str] = None
    influx_token: Optional[str] = None
    influx_verify: Optional[bool] = None
    mtu: Optional[int] = None
    opentelemetry_compression: Optional[str] = None
    opentelemetry_headers: Optional[str] = None
    opentelemetry_max_body_size: Optional[int] = None
    opentelemetry_path: Optional[str] = None
    opentelemetry_proto: Optional[str] = None
    opentelemetry_resource_attributes: Optional[str] = None
    opentelemetry_timeout: Optional[int] = None
    opentelemetry_verify_ssl: Optional[bool] = None
    port: Optional[int] = None
    server: Optional[str] = None
    timeout: Optional[int] = None
    type: Optional[str] = None  # "graphite" | "influxdb" | "opentelemetry"


class OciImageSpec(BaseModel):
    name: str
    node_name: str
    datastore_id: str
    reference: str  # e.g. "docker.io/library/alpine:latest"
    file_name: Optional[str] = None
    overwrite: Optional[bool] = None
    overwrite_unmanaged: Optional[bool] = None
    upload_timeout: Optional[int] = None


class AptRepositorySpec(BaseModel):
    name: str
    node: str
    file_path: str  # e.g. "/etc/apt/sources.list.d/pve.list"
    index: int  # 0-based index within the file
    enabled: Optional[bool] = None


class PoolMembershipSpec(BaseModel):
    name: str
    pool_id: str
    vm_id: Optional[int] = None
    storage_id: Optional[str] = None


class ClusterMiscConfig(BaseModel):
    options: Optional[ClusterOptionsSpec] = None
    hw_mapping_pci: list[HwMappingPciSpec] = []
    hw_mapping_usb: list[HwMappingUsbSpec] = []
    hw_mapping_dir: list[HwMappingDirSpec] = []
    metrics_servers: list[MetricsServerSpec] = []
    oci_images: list[OciImageSpec] = []
    apt_repositories: list[AptRepositorySpec] = []
    pool_memberships: list[PoolMembershipSpec] = []


# ============================================================================
# INVENTORY (главная модель)
# ============================================================================


class Inventory(BaseModel):
    provider: Provider
    vms: list[VMSpec] = []
    containers: list[LxcSpec] = []
    pools: list[PoolSpec] = []
    ha_groups: list[HaGroupSpec] = []
    ha_rules: list[HaRuleSpec] = []
    backups: list[BackupJobSpec] = []
    replications: list[ReplicationSpec] = []
    rbac: Optional[RbacConfig] = None
    firewall: Optional[FirewallConfig] = None
    acme: Optional[AcmeConfig] = None
    cluster_misc: Optional[ClusterMiscConfig] = None
    downloads: list[DownloadFileSpec] = []
    uploads: list[UploadFileSpec] = []
    cloned_vms: list[ClonedVmSpec] = []
    sdn: Optional[SdnConfig] = None
    network_bridges: list[NetworkBridgeSpec] = []
    network_vlans: list[NetworkVlanSpec] = []
    node_dns: list[NodeDnsSpec] = []
    node_hosts: list[NodeHostsSpec] = []
    node_time: list[NodeTimeSpec] = []
    storages: Optional[StorageConfig] = None

    @model_validator(mode="after")
    def validate_ha_groups(self) -> Inventory:
        ha_group_names = {g.name for g in self.ha_groups}
        for vm in self.vms:
            if vm.ha and vm.ha.group and vm.ha.group not in ha_group_names:
                raise ValueError(
                    f"VM '{vm.name}': ha.group '{vm.ha.group}' not found in ha_groups"
                )
        return self
