# AGENTS.md

Pulumi-based infrastructure-as-code tool for Proxmox VE. Users write an `inventory.yaml` (or `inventory.yaml.j2`) describing their desired state; this project renders it and applies it via Pulumi using the `pulumi-proxmoxve` SDK.

## Deep-dive references

| Topic | File |
| --- | --- |
| Runtime pipeline (Docker → Jinja2 → Pulumi) | [agents/architecture.md](agents/architecture.md) |
| Inventory model and all top-level fields | [agents/inventory.md](agents/inventory.md) |
| Builder pattern and adding new resource types | [agents/builders.md](agents/builders.md) |
| Jinja2 render helpers and data-source functions | [agents/jinja2.md](agents/jinja2.md) |

## File map

```text
pulumi-proxmoxve/
├── Dockerfile                    # image: OracleLinux 10 + Pulumi + pulumi-proxmoxve + rich
├── entrypoint.py                 # renders inventory.yaml.j2, then runs pulumi up (rich UI)
├── inventory.yaml.j2             # РАБОЧИЙ файл пользователя — не добавлять сюда примеры
├── render_helpers.py             # Jinja2 globals — Proxmox REST API helpers
├── sources/
│   ├── models.py                 # ALL Pydantic models; Inventory is the root
│   ├── loader.py                 # load_inventory(path) → Inventory
│   ├── project/
│   │   ├── Pulumi.yaml
│   │   └── __main__.py           # Pulumi program entry point
│   ├── vm.py                     # build_vm()
│   ├── lxc.py                    # build_container()
│   ├── cloned_vm.py              # build_cloned_vm()
│   ├── cloud_init.py             # build_cloud_init_file()
│   ├── ssh_key.py                # build_ssh_key()
│   ├── pool.py                   # build_pool()
│   ├── ha.py                     # build_ha_group/resource/rule()
│   ├── backup.py                 # build_backup_job()
│   ├── replication.py            # build_replication()
│   ├── rbac.py                   # build_rbac()
│   ├── firewall.py               # build_firewall()
│   ├── acme.py                   # build_acme()
│   ├── cluster_misc.py           # build_cluster_misc()
│   ├── sdn.py                    # build_sdn_zone/vnet/subnet/applier/fabric_*()
│   ├── network.py                # build_linux_bridge/vlan()
│   ├── node_config.py            # build_dns/hosts/time()
│   ├── storage.py                # build_storages()
│   ├── download.py               # build_download_file()
│   └── upload.py                 # build_upload_file()
└── docs/
    ├── inventory.yaml.j2         # полный аннотированный пример всех полей inventory
    └── jinja_functions.md        # reference for all render_helpers.py functions
```

## Before committing

Always run before every commit to avoid CI failures:

```bash
uvx ruff format .
uvx ruff check .
```

## Critical rules

- **Never pass `None` to SDK kwargs.** All optional fields must be guarded: `if spec.foo is not None`.
- **`sources/` is the Python path root.** Imports inside `sources/project/__main__.py` resolve from `sources/` (`from models import ...`, not `from sources.models import ...`).
- **`render_helpers.py` uses stdlib only** (`urllib.request`, `ssl`, `json`). Do not add third-party imports — `requests` is not installed. Third-party deps belong in `entrypoint.py`, not here.
- **`entrypoint.py` uses `rich`** for all terminal output (panels, rules, spinners, tables). It imports `render_helpers.JINJA2_GLOBALS` directly — no subprocess/heredoc.
- **Adding a resource type requires 4 files** — see [agents/builders.md](agents/builders.md).
- **`Inventory` in `sources/models.py` is the only root model.** Every new top-level section must be added there.
- **`pulumi-proxmoxve` version is pinned to `8.2.1`** in `Dockerfile` (defaults overridden by the release tag in CI). Check the SDK for available resource/arg names before writing builder code.
