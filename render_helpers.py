import json
import ssl
import types
import urllib.parse
import urllib.request


def proxmox_get(endpoint, api_token, path, insecure=False, **params):
    url = endpoint.rstrip("/") + "/api2/json" + path
    if params:
        url += "?" + urllib.parse.urlencode(
            {k: v for k, v in params.items() if v is not None}
        )
    req = urllib.request.Request(
        url, headers={"Authorization": f"PVEAPIToken={api_token}"}
    )
    ctx = ssl.create_default_context()
    if insecure:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, context=ctx) as resp:
        return json.loads(resp.read())["data"]


def _g(endpoint, api_token, path, insecure=False, **params):
    return proxmox_get(endpoint, api_token, path, insecure, **params)


# ── Версия ────────────────────────────────────────────────────────────────────


def get_version(endpoint, api_token, insecure=False):
    return _g(endpoint, api_token, "/version", insecure)


get_version_legacy = get_version


# ── Узлы ──────────────────────────────────────────────────────────────────────


def get_nodes_legacy(endpoint, api_token, insecure=False):
    return _g(endpoint, api_token, "/nodes", insecure)


def get_node_legacy(endpoint, api_token, node_name, insecure=False):
    return _g(endpoint, api_token, f"/nodes/{node_name}/status", insecure)


# ── Виртуальные машины ────────────────────────────────────────────────────────


def get_vms_legacy(endpoint, api_token, node_name, insecure=False):
    return _g(endpoint, api_token, f"/nodes/{node_name}/qemu", insecure)


def get_vm_legacy(endpoint, api_token, node_name, vm_id, insecure=False):
    return _g(endpoint, api_token, f"/nodes/{node_name}/qemu/{vm_id}/config", insecure)


def get_vm(endpoint, api_token, node_name, vm_id, insecure=False):
    return _g(endpoint, api_token, f"/nodes/{node_name}/qemu/{vm_id}/config", insecure)


get_vm2_legacy = get_vm_legacy


# ── Контейнеры LXC ────────────────────────────────────────────────────────────


def get_containers_legacy(endpoint, api_token, node_name, insecure=False):
    return _g(endpoint, api_token, f"/nodes/{node_name}/lxc", insecure)


def get_container_legacy(endpoint, api_token, node_name, vm_id, insecure=False):
    return _g(endpoint, api_token, f"/nodes/{node_name}/lxc/{vm_id}/config", insecure)


# ── Хранилища ─────────────────────────────────────────────────────────────────


def get_datastores(endpoint, api_token, node_name, insecure=False):
    return _g(endpoint, api_token, f"/nodes/{node_name}/storage", insecure)


get_datastores_legacy = get_datastores


# ── Конфигурация узла ─────────────────────────────────────────────────────────


def get_dns_legacy(endpoint, api_token, node_name, insecure=False):
    return _g(endpoint, api_token, f"/nodes/{node_name}/dns", insecure)


def get_hosts_legacy(endpoint, api_token, node_name, insecure=False):
    return _g(endpoint, api_token, f"/nodes/{node_name}/hosts", insecure)


def get_time_legacy(endpoint, api_token, node_name, insecure=False):
    return _g(endpoint, api_token, f"/nodes/{node_name}/time", insecure)


# ── Файлы storage ─────────────────────────────────────────────────────────────


def get_files(endpoint, api_token, node_name, datastore_id, insecure=False):
    return _g(
        endpoint,
        api_token,
        f"/nodes/{node_name}/storage/{datastore_id}/content",
        insecure,
    )


def get_file(endpoint, api_token, node_name, datastore_id, file_id, insecure=False):
    encoded = urllib.parse.quote(file_id, safe="")
    return _g(
        endpoint,
        api_token,
        f"/nodes/{node_name}/storage/{datastore_id}/content/{encoded}",
        insecure,
    )


get_file_legacy = get_file


# ── HA ────────────────────────────────────────────────────────────────────────


def get_hagroups(endpoint, api_token, insecure=False):
    return _g(endpoint, api_token, "/cluster/ha/groups", insecure)


def get_hagroup(endpoint, api_token, group, insecure=False):
    return _g(endpoint, api_token, f"/cluster/ha/groups/{group}", insecure)


def get_haresources(endpoint, api_token, insecure=False):
    return _g(endpoint, api_token, "/cluster/ha/resources", insecure)


def get_haresource(endpoint, api_token, resource_id, insecure=False):
    return _g(endpoint, api_token, f"/cluster/ha/resources/{resource_id}", insecure)


get_hagroups_legacy = get_hagroups
get_hagroup_legacy = get_hagroup
get_haresources_legacy = get_haresources
get_haresource_legacy = get_haresource


# ── Пулы ──────────────────────────────────────────────────────────────────────


def get_pools_legacy(endpoint, api_token, insecure=False):
    return _g(endpoint, api_token, "/pools", insecure)


def get_pool_legacy(endpoint, api_token, pool_id, insecure=False):
    return _g(endpoint, api_token, f"/pools/{pool_id}", insecure)


# ── RBAC ──────────────────────────────────────────────────────────────────────


def get_roles_legacy(endpoint, api_token, insecure=False):
    return _g(endpoint, api_token, "/access/roles", insecure)


def get_role_legacy(endpoint, api_token, role_id, insecure=False):
    return _g(endpoint, api_token, f"/access/roles/{role_id}", insecure)


def get_groups_legacy(endpoint, api_token, insecure=False):
    return _g(endpoint, api_token, "/access/groups", insecure)


def get_group_legacy(endpoint, api_token, group_id, insecure=False):
    return _g(endpoint, api_token, f"/access/groups/{group_id}", insecure)


def get_users_legacy(endpoint, api_token, insecure=False):
    return _g(endpoint, api_token, "/access/users", insecure)


def get_user_legacy(endpoint, api_token, user_id, insecure=False):
    return _g(endpoint, api_token, f"/access/users/{user_id}", insecure)


# ── Репликация ────────────────────────────────────────────────────────────────


def get_replications(endpoint, api_token, insecure=False):
    return _g(endpoint, api_token, "/cluster/replication", insecure)


def get_replication(endpoint, api_token, id, insecure=False):
    return _g(endpoint, api_token, f"/cluster/replication/{id}", insecure)


get_replications_legacy = get_replications
get_replication_legacy = get_replication


# ── acme ──────────────────────────────────────────────────────────────────────


def _acme_get_accounts(endpoint, api_token, insecure=False):
    return _g(endpoint, api_token, "/cluster/acme/account", insecure)


def _acme_get_account(endpoint, api_token, name, insecure=False):
    return _g(endpoint, api_token, f"/cluster/acme/account/{name}", insecure)


def _acme_get_plugins(endpoint, api_token, insecure=False):
    return _g(endpoint, api_token, "/cluster/acme/plugins", insecure)


def _acme_get_plugin(endpoint, api_token, plugin, insecure=False):
    return _g(endpoint, api_token, f"/cluster/acme/plugins/{plugin}", insecure)


acme = types.SimpleNamespace(
    get_accounts=_acme_get_accounts,
    get_account=_acme_get_account,
    get_plugins=_acme_get_plugins,
    get_plugin=_acme_get_plugin,
)


# ── apt ───────────────────────────────────────────────────────────────────────


def _apt_get_repository(endpoint, api_token, node_name, insecure=False):
    return _g(endpoint, api_token, f"/nodes/{node_name}/apt/repositories", insecure)


apt = types.SimpleNamespace(
    get_repository=_apt_get_repository,
    standard=types.SimpleNamespace(
        get_repository=_apt_get_repository,
    ),
)


# ── backup ────────────────────────────────────────────────────────────────────


def _backup_get_jobs(endpoint, api_token, insecure=False):
    return _g(endpoint, api_token, "/cluster/backup", insecure)


backup = types.SimpleNamespace(
    get_jobs=_backup_get_jobs,
)


# ── hardware ──────────────────────────────────────────────────────────────────


def _hardware_get_mappings(endpoint, api_token, insecure=False):
    return _g(endpoint, api_token, "/cluster/mapping", insecure)


def _hardware_mapping_get_pci(endpoint, api_token, name, insecure=False):
    return _g(endpoint, api_token, f"/cluster/mapping/pci/{name}", insecure)


def _hardware_mapping_get_usb(endpoint, api_token, name, insecure=False):
    return _g(endpoint, api_token, f"/cluster/mapping/usb/{name}", insecure)


hardware = types.SimpleNamespace(
    get_mappings=_hardware_get_mappings,
    mapping=types.SimpleNamespace(
        get_pci=_hardware_mapping_get_pci,
        get_usb=_hardware_mapping_get_usb,
    ),
)


# ── metrics ───────────────────────────────────────────────────────────────────


def _metrics_get_server(endpoint, api_token, name, insecure=False):
    return _g(endpoint, api_token, f"/cluster/metrics/server/{name}", insecure)


metrics = types.SimpleNamespace(
    get_server=_metrics_get_server,
)


# ── sdn ───────────────────────────────────────────────────────────────────────


def _sdn_get_zones(endpoint, api_token, insecure=False):
    return _g(endpoint, api_token, "/cluster/sdn/zones", insecure)


def _sdn_get_vnets(endpoint, api_token, insecure=False):
    return _g(endpoint, api_token, "/cluster/sdn/vnets", insecure)


def _sdn_get_vnet(endpoint, api_token, id, insecure=False):
    return _g(endpoint, api_token, f"/cluster/sdn/vnets/{id}", insecure)


def _sdn_get_subnet(endpoint, api_token, vnet, cidr, insecure=False):
    encoded_cidr = urllib.parse.quote(cidr, safe="")
    return _g(
        endpoint,
        api_token,
        f"/cluster/sdn/vnets/{vnet}/subnets/{encoded_cidr}",
        insecure,
    )


def _sdn_get_zone(endpoint, api_token, id, insecure=False):
    return _g(endpoint, api_token, f"/cluster/sdn/zones/{id}", insecure)


def _sdn_fabric_get(endpoint, api_token, id, insecure=False):
    return _g(endpoint, api_token, f"/cluster/sdn/fabrics/{id}", insecure)


def _sdn_fabric_node_get(endpoint, api_token, fabric_id, node_id, insecure=False):
    return _g(
        endpoint,
        api_token,
        f"/cluster/sdn/fabrics/{fabric_id}/nodes/{node_id}",
        insecure,
    )


sdn = types.SimpleNamespace(
    get_zones=_sdn_get_zones,
    get_vnets=_sdn_get_vnets,
    get_vnet=_sdn_get_vnet,
    get_subnet=_sdn_get_subnet,
    get_zone=_sdn_get_zone,
    zone=types.SimpleNamespace(
        get_evpn=_sdn_get_zone,
        get_simple=_sdn_get_zone,
        get_vlan=_sdn_get_zone,
        get_vxlan=_sdn_get_zone,
        get_qinq=_sdn_get_zone,
    ),
    fabric=types.SimpleNamespace(
        get_openfabric=_sdn_fabric_get,
        get_ospf=_sdn_fabric_get,
        node=types.SimpleNamespace(
            get_openfabric=_sdn_fabric_node_get,
            get_ospf=_sdn_fabric_node_get,
        ),
    ),
)


# ── Реестр Jinja2-глобалов ────────────────────────────────────────────────────

JINJA2_GLOBALS = {
    "proxmox_get": proxmox_get,
    # Версия
    "get_version": get_version,
    "get_version_legacy": get_version_legacy,
    # Узлы
    "get_nodes_legacy": get_nodes_legacy,
    "get_node_legacy": get_node_legacy,
    # VMs
    "get_vms_legacy": get_vms_legacy,
    "get_vm_legacy": get_vm_legacy,
    "get_vm": get_vm,
    "get_vm2_legacy": get_vm2_legacy,
    # Контейнеры
    "get_containers_legacy": get_containers_legacy,
    "get_container_legacy": get_container_legacy,
    # Хранилища
    "get_datastores": get_datastores,
    "get_datastores_legacy": get_datastores_legacy,
    # Конфигурация узла
    "get_dns_legacy": get_dns_legacy,
    "get_hosts_legacy": get_hosts_legacy,
    "get_time_legacy": get_time_legacy,
    # Файлы
    "get_files": get_files,
    "get_file": get_file,
    "get_file_legacy": get_file_legacy,
    # HA
    "get_hagroups": get_hagroups,
    "get_hagroups_legacy": get_hagroups_legacy,
    "get_hagroup": get_hagroup,
    "get_hagroup_legacy": get_hagroup_legacy,
    "get_haresources": get_haresources,
    "get_haresources_legacy": get_haresources_legacy,
    "get_haresource": get_haresource,
    "get_haresource_legacy": get_haresource_legacy,
    # Пулы
    "get_pools_legacy": get_pools_legacy,
    "get_pool_legacy": get_pool_legacy,
    # RBAC
    "get_roles_legacy": get_roles_legacy,
    "get_role_legacy": get_role_legacy,
    "get_groups_legacy": get_groups_legacy,
    "get_group_legacy": get_group_legacy,
    "get_users_legacy": get_users_legacy,
    "get_user_legacy": get_user_legacy,
    # Репликация
    "get_replications": get_replications,
    "get_replications_legacy": get_replications_legacy,
    "get_replication": get_replication,
    "get_replication_legacy": get_replication_legacy,
    # Пространства имён
    "acme": acme,
    "apt": apt,
    "backup": backup,
    "hardware": hardware,
    "metrics": metrics,
    "sdn": sdn,
}
