# Builders

Each resource domain lives in a dedicated `sources/*.py` module. Every builder function:

- Accepts a `*Spec` (or `*Config`) Pydantic model and a `proxmox.Provider`
- Creates one or more Pulumi resources as side effects
- Returns the primary resource (or `None` if there is no single primary resource)

## Builder function signature

```python
def build_x(spec: XSpec, provider: proxmox.Provider) -> proxmox.XResource:
    return proxmox.XResource(
        spec.name,
        field_a=spec.field_a,
        field_b=spec.field_b if spec.field_b is not None else None,
        opts=pulumi.ResourceOptions(provider=provider),
    )
```

**Critical:** Never pass `None` as a keyword argument to an SDK class. Either guard with `if spec.field is not None` and pass only when set, or use a dict and `**kwargs` pattern:

```python
kwargs = {"required_field": spec.required}
if spec.optional is not None:
    kwargs["optional"] = spec.optional
return proxmox.XResource(spec.name, **kwargs, opts=pulumi.ResourceOptions(provider=provider))
```

The SDK raises a validation error if an optional param receives `None`.

## 4-step pattern for a new resource type

### Step 1 — Models (`sources/models.py`)

Add `XSpec` (leaf) and optionally `XConfig` (container with multiple lists):

```python
class XSpec(BaseModel):
    name: str
    required_field: str
    optional_field: Optional[str] = None

class XConfig(BaseModel):         # only needed if multiple sub-types
    items: list[XSpec] = []
```

Add to `Inventory`:

```python
class Inventory(BaseModel):
    ...
    x_things: list[XSpec] = []           # for simple lists
    # OR
    x_config: Optional[XConfig] = None   # for grouped optional sections
```

### Step 2 — Builder module (`sources/x.py`)

```python
import pulumi
import pulumi_proxmoxve as proxmox
from models import XSpec

def build_x(spec: XSpec, provider: proxmox.Provider) -> proxmox.XResource:
    return proxmox.XResource(
        spec.name,
        required_field=spec.required_field,
        opts=pulumi.ResourceOptions(provider=provider),
    )
```

### Step 3 — Main entry point (`sources/project/__main__.py`)

Import and call in dependency order:

```python
from x import build_x

# simple list
for spec in inv.x_things:
    build_x(spec, provider)

# optional grouped section
if inv.x_config:
    for spec in inv.x_config.items:
        build_x(spec, provider)
```

### Step 4 — Docs (`docs/inventory.yaml.j2`)

Add a commented example block showing realistic values for every field.

## Dependency ordering in `__main__.py`

Current order (top → bottom):

1. RBAC (roles → groups → users → tokens → ACLs → realms)
2. Firewall
3. ACME (DNS plugins → accounts → certificates → node certificates)
4. Cluster misc (options → HW mappings → metrics → OCI → APT → pool memberships)
5. Storages
6. Network bridges & VLANs
7. Node config (DNS / hosts / time)
8. Downloads
9. Pools
10. HA groups → HA fencing rules
11. Backup jobs
12. Replication
13. SDN (zones → vnets → subnets → fabrics → fabric nodes → applier)
14. SSH key + cloud-init file
15. VMs (templates first, then clones; HA resources inline with each VM)
16. LXC containers

When adding a new section, place it before any section that depends on it.

## Resource naming

The first positional argument to every SDK resource is its **Pulumi logical name** (used for state tracking). Use `spec.name` for it. This name must be unique within a stack — it does not have to match the Proxmox resource ID.

## `depends_on` pattern

When a resource must be created after another Pulumi resource (not just a Proxmox-side dependency):

```python
proxmox.XResource(
    spec.name,
    ...,
    opts=pulumi.ResourceOptions(provider=provider, depends_on=[other_resource]),
)
```

See the VM two-pass pattern in `__main__.py` (templates first, then clones) for a real example.

## Existing builder modules

| File | Builder functions |
|---|---|
| `vm.py` | `build_vm` |
| `lxc.py` | `build_container` |
| `cloud_init.py` | `build_cloud_init_file` |
| `ssh_key.py` | `build_ssh_key` |
| `pool.py` | `build_pool` |
| `ha.py` | `build_ha_group`, `build_ha_resource`, `build_ha_rule` |
| `backup.py` | `build_backup_job` |
| `replication.py` | `build_replication` |
| `rbac.py` | `build_rbac` (dispatcher calling sub-builders internally) |
| `firewall.py` | `build_firewall` (dispatcher) |
| `acme.py` | `build_acme` (dispatcher) |
| `cluster_misc.py` | `build_cluster_misc` (dispatcher) |
| `sdn.py` | `build_sdn_zone`, `build_sdn_vnet`, `build_sdn_subnet`, `build_sdn_applier`, `build_sdn_fabric_openfabric`, `build_sdn_fabric_ospf`, `build_sdn_fabric_node_openfabric`, `build_sdn_fabric_node_ospf` |
| `network.py` | `build_linux_bridge`, `build_linux_vlan` |
| `node_config.py` | `build_dns`, `build_hosts`, `build_time` |
| `storage.py` | `build_storages` (dispatcher) |
| `download.py` | `build_download_file` |
