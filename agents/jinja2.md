# Jinja2 render helpers

`render_helpers.py` (project root) is copied into the Docker image at `/render_helpers.py`. It provides Proxmox REST API query functions that can be called inside `inventory.yaml.j2` at render time — before Pulumi runs.

## How functions reach templates

`entrypoint.sh` inline heredoc:

```python
sys.path.insert(0, '/')                  # /render_helpers.py → importable
from render_helpers import JINJA2_GLOBALS
jenv.globals.update(JINJA2_GLOBALS)      # all 45 names injected into Jinja2
```

Templates call them directly by name:

```yaml
{% set nodes = get_nodes_legacy(env.PVE_ENDPOINT, env.PVE_TOKEN) %}
```

## Transport

All functions use Python stdlib only (`urllib.request`, `ssl`, `json`). The `requests` library is not available in the image.

Every function ultimately calls:

```python
def proxmox_get(endpoint, api_token, path, insecure=False, **params):
    url = endpoint.rstrip('/') + '/api2/json' + path
    # optional query params appended
    req = urllib.request.Request(url, headers={'Authorization': f'PVEAPIToken={api_token}'})
    # ssl context: check_hostname=False + CERT_NONE when insecure=True
    return json.loads(resp.read())['data']   # unwrapped — raw REST response
```

Return value is always the unwrapped `data` field from `{"data": ...}`.

## Function signature convention

```text
get_X(endpoint, api_token, [resource_id, ...], insecure=False) → dict | list[dict]
```

- `endpoint` — full base URL, e.g. `"https://pve.example.com:8006"`
- `api_token` — `"user@realm!token-id=secret"`
- `insecure` — skip TLS verification

## Utility globals (no API call)

| Name | Source | Description |
| --- | --- | --- |
| `load_yaml` | `entrypoint.py` | Load a YAML file by path → Python object; supports `.j2` files (rendered first) |

### `load_yaml(path)` — YAML-файл в переменную

```jinja2
{%- set d = load_yaml('vm_defaults.yaml') %}
  bios: {{ d.bios }}
```

Path is relative to the template directory. If the file ends in `.j2`, it is rendered as a Jinja2 template first.

---

## JINJA2_GLOBALS — flat functions

| Name | REST path | Returns |
|---|---|---|
| `proxmox_get` | arbitrary path | raw response |
| `get_version` / `get_version_legacy` | `GET /version` | dict |
| `get_nodes_legacy` | `GET /nodes` | list[dict] |
| `get_node_legacy` | `GET /nodes/{node}/status` | dict |
| `get_vms_legacy` | `GET /nodes/{node}/qemu` | list[dict] |
| `get_vm` / `get_vm_legacy` / `get_vm2_legacy` | `GET /nodes/{node}/qemu/{id}/config` | dict |
| `get_containers_legacy` | `GET /nodes/{node}/lxc` | list[dict] |
| `get_container_legacy` | `GET /nodes/{node}/lxc/{id}/config` | dict |
| `get_datastores` / `get_datastores_legacy` | `GET /nodes/{node}/storage` | list[dict] |
| `get_dns_legacy` | `GET /nodes/{node}/dns` | dict |
| `get_hosts_legacy` | `GET /nodes/{node}/hosts` | dict |
| `get_time_legacy` | `GET /nodes/{node}/time` | dict |
| `get_files` | `GET /nodes/{node}/storage/{ds}/content` | list[dict] |
| `get_file` / `get_file_legacy` | `GET /nodes/{node}/storage/{ds}/content/{id}` | dict |
| `get_hagroups` / `get_hagroups_legacy` | `GET /cluster/ha/groups` | list[dict] |
| `get_hagroup` / `get_hagroup_legacy` | `GET /cluster/ha/groups/{group}` | dict |
| `get_haresources` / `get_haresources_legacy` | `GET /cluster/ha/resources` | list[dict] |
| `get_haresource` / `get_haresource_legacy` | `GET /cluster/ha/resources/{id}` | dict |
| `get_pools_legacy` | `GET /pools` | list[dict] |
| `get_pool_legacy` | `GET /pools/{id}` | dict |
| `get_roles_legacy` | `GET /access/roles` | list[dict] |
| `get_role_legacy` | `GET /access/roles/{id}` | dict |
| `get_groups_legacy` | `GET /access/groups` | list[dict] |
| `get_group_legacy` | `GET /access/groups/{id}` | dict |
| `get_users_legacy` | `GET /access/users` | list[dict] |
| `get_user_legacy` | `GET /access/users/{id}` | dict |
| `get_replications` / `get_replications_legacy` | `GET /cluster/replication` | list[dict] |
| `get_replication` / `get_replication_legacy` | `GET /cluster/replication/{id}` | dict |

## JINJA2_GLOBALS — namespaced objects (SimpleNamespace)

| Name | Methods | REST path |
|---|---|---|
| `acme` | `.get_accounts(ep, tok)` | `GET /cluster/acme/account` |
| | `.get_account(ep, tok, name)` | `GET /cluster/acme/account/{name}` |
| | `.get_plugins(ep, tok)` | `GET /cluster/acme/plugins` |
| | `.get_plugin(ep, tok, plugin)` | `GET /cluster/acme/plugins/{plugin}` |
| `apt` | `.get_repository(ep, tok, node)` | `GET /nodes/{node}/apt/repositories` |
| | `.standard.get_repository(ep, tok, node)` | same |
| `backup` | `.get_jobs(ep, tok)` | `GET /cluster/backup` |
| `hardware` | `.get_mappings(ep, tok)` | `GET /cluster/mapping` |
| | `.mapping.get_pci(ep, tok, name)` | `GET /cluster/mapping/pci/{name}` |
| | `.mapping.get_usb(ep, tok, name)` | `GET /cluster/mapping/usb/{name}` |
| `metrics` | `.get_server(ep, tok, name)` | `GET /cluster/metrics/server/{name}` |
| `sdn` | `.get_zones(ep, tok)` | `GET /cluster/sdn/zones` |
| | `.get_zone(ep, tok, id)` | `GET /cluster/sdn/zones/{id}` |
| | `.get_vnets(ep, tok)` | `GET /cluster/sdn/vnets` |
| | `.get_vnet(ep, tok, id)` | `GET /cluster/sdn/vnets/{id}` |
| | `.get_subnet(ep, tok, vnet, cidr)` | `GET /cluster/sdn/vnets/{vnet}/subnets/{cidr}` (CIDR is URL-encoded) |
| | `.zone.get_evpn/simple/vlan/vxlan/qinq(ep, tok, id)` | same as `.get_zone` |
| | `.fabric.get_openfabric/ospf(ep, tok, id)` | `GET /cluster/sdn/fabrics/{id}` |
| | `.fabric.node.get_openfabric/ospf(ep, tok, fabric, node)` | `GET /cluster/sdn/fabrics/{fabric}/nodes/{node}` |

Full field-level documentation for every return value: [docs/jinja_functions.md](../docs/jinja_functions.md).

## Adding a new function

1. Define `def _x_get_thing(endpoint, api_token, ..., insecure=False)` calling `_g(...)`.
2. If it fits an existing namespace, add it to the `types.SimpleNamespace(...)` call.
3. If it's a top-level function, add a module-level alias if a legacy variant is needed.
4. Register it in `JINJA2_GLOBALS` at the bottom of `render_helpers.py`.

## Using default filter for optional data

Functions raise `urllib.error.HTTPError` on failure. Use Jinja2's `default` filter to handle missing resources gracefully:

```yaml
{% set cert = acme.get_account(ep, tok, "default") | default(none) %}
```
