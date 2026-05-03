# Inventory

`Inventory` in [sources/models.py](../sources/models.py) is the root Pydantic model. `load_inventory()` in [sources/loader.py](../sources/loader.py) does `yaml.safe_load` → `Inventory(**data)`.

## Top-level fields

| YAML key | Type | Description |
| --- | --- | --- |
| `provider` | `Provider` | **Required.** Proxmox endpoint + credentials |
| `vms` | `list[VMSpec]` | QEMU virtual machines |
| `containers` | `list[LxcSpec]` | LXC containers |
| `pools` | `list[PoolSpec]` | Resource pools |
| `ha_groups` | `list[HaGroupSpec]` | HA groups |
| `ha_rules` | `list[HaRuleSpec]` | HA fencing rules |
| `backups` | `list[BackupJobSpec]` | Cluster-level backup jobs |
| `replications` | `list[ReplicationSpec]` | VM/CT replication jobs |
| `downloads` | `list[DownloadFileSpec]` | ISO / template downloads (Proxmox скачивает по URL) |
| `uploads` | `list[UploadFileSpec]` | Загрузка файлов с локальной машины через API |
| `cloned_vms` | `list[ClonedVmSpec]` | Облегчённое клонирование VM (`cloned.Vm/VmLegacy`) |
| `network_bridges` | `list[NetworkBridgeSpec]` | Linux bridges on nodes |
| `network_vlans` | `list[NetworkVlanSpec]` | Linux VLANs on nodes |
| `node_dns` | `list[NodeDnsSpec]` | Per-node DNS config |
| `node_hosts` | `list[NodeHostsSpec]` | Per-node /etc/hosts entries |
| `node_time` | `list[NodeTimeSpec]` | Per-node timezone |
| `rbac` | `Optional[RbacConfig]` | Roles, groups, users, tokens, ACLs, realms |
| `firewall` | `Optional[FirewallConfig]` | Cluster / node / VM firewall |
| `acme` | `Optional[AcmeConfig]` | ACME DNS plugins, accounts, certificates |
| `cluster_misc` | `Optional[ClusterMiscConfig]` | Options, HW mappings, metrics, OCI, APT, pool membership |
| `sdn` | `Optional[SdnConfig]` | SDN zones, vnets, subnets, fabrics, applier |
| `storages` | `Optional[StorageConfig]` | NFS/CIFS/LVM/ZFS/PBS/Dir storage backends |

## Provider

```yaml
provider:
  endpoint: "https://pve.example.com:8006"
  insecure: true          # skip TLS verification
  api_token: "user@pam!token-id=secret"
```

## Pydantic conventions used throughout models.py

- All spec classes inherit from `pydantic.BaseModel`.
- Optional fields use `Optional[T] = None`. If a field is `None`, the builder **must not** pass it to the SDK (the SDK raises an error on unexpected `None`).
- List fields default to `[]` — never `None`.
- `Optional[XConfig]` section fields (rbac, firewall, acme, …) default to `None` — the builder is skipped entirely with `if inv.X:`.
- Field names use **snake_case** matching the SDK parameter names. Where the inventory key differs from the SDK arg, the mapping is explicit in the builder (e.g. `datastore` → `datastore_id`).

## Adding a new top-level section

1. Create `XSpec` (and any nested `*Spec`) classes in `sources/models.py`.
2. Add `x_things: Optional[XConfig] = None` (or `list[XSpec] = []`) to `Inventory`.
3. Import and call `build_x()` in `sources/project/__main__.py`.
4. Add an example block to `docs/inventory.yaml.j2`.

The full 4-step process is documented in [agents/builders.md](builders.md).

## Validation

`Inventory` has one `@model_validator`: it checks that every `vm.ha.group` references a name that exists in `ha_groups`. Add similar cross-field validators here when introducing relationships between sections.

## Full annotated example

See [docs/inventory.yaml.j2](../docs/inventory.yaml.j2) — it demonstrates every field with realistic values and Jinja2 data-source calls.
