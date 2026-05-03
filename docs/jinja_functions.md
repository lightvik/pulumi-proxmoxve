# Jinja2-функции для запросов к Proxmox API

Функции доступны в шаблоне `inventory.yaml.j2` без импорта. Каждая делает
`GET`-запрос к Proxmox REST API и возвращает содержимое поля `data` ответа
в виде `dict` или `list[dict]`.

При ошибке HTTP или недоступности сервера рендер упадёт с исключением.
Чтобы подставить значение по умолчанию, используйте фильтр Jinja2 `default`:

```yaml
{% set nodes = get_nodes_legacy(ep, tok) | default([]) %}
```

---

## Общие параметры

Все функции принимают одинаковые первые параметры:

| Параметр | Тип | Описание |
|----------|-----|----------|
| `endpoint` | str | URL Proxmox API, например `https://192.168.1.1:8006` |
| `api_token` | str | Токен в формате `user@realm!token-id=secret` |
| `insecure` | bool | Отключить проверку TLS-сертификата (по умолчанию `False`) |

Удобный приём — вынести их в переменные шаблона:

```yaml
{% set ep  = env.PROXMOX_ENDPOINT %}
{% set tok = env.PROXMOX_TOKEN %}
```

---

## Утилиты (без запросов к API)

### `load_yaml(path)`

Читает YAML-файл по пути `path` и возвращает Python-объект. Путь — относительно директории шаблона. Если файл оканчивается на `.j2`, он сначала рендерится как Jinja2-шаблон.

**Пример:**
```jinja2
{%- set d = load_yaml('vm_defaults.yaml') %}
  bios: {{ d.bios }}
```

> `load_yaml` зарегистрирован в `entrypoint.py`.

---

## `proxmox_get(endpoint, api_token, path, insecure=False, **params)`

Базовая функция. Выполняет произвольный GET-запрос.

**Параметры:**

| Параметр | Тип | Описание |
|----------|-----|----------|
| `path` | str | Путь после `/api2/json`, например `/nodes` |
| `**params` | — | Дополнительные query-параметры |

**Возвращает:** `dict` или `list[dict]` — содержимое поля `data` ответа.

**Пример:**
```yaml
{% set vms = proxmox_get(ep, tok, '/nodes/pve/qemu') %}
```

---

## Версия кластера

### `get_version(endpoint, api_token, insecure=False)`

**REST:** `GET /api2/json/version`  
**Псевдоним:** `get_version_legacy`

**Возвращает:** `dict`

| Поле | Тип | Описание |
|------|-----|----------|
| `version` | str | Версия Proxmox VE, например `8.3.1` |
| `release` | str | Версия Debian |
| `repoid` | str | Идентификатор репозитория |

**Пример:**
```yaml
{% set ver = get_version(ep, tok) %}
# Proxmox {{ ver.version }}
```

---

## Узлы

### `get_nodes_legacy(endpoint, api_token, insecure=False)`

**REST:** `GET /api2/json/nodes`

**Возвращает:** `list[dict]`

| Поле | Тип | Описание |
|------|-----|----------|
| `node` | str | Имя узла |
| `status` | str | `online` \| `offline` |
| `cpu` | float | Загрузка CPU (0.0–1.0) |
| `maxcpu` | int | Количество логических CPU |
| `mem` | int | Использованная RAM, байт |
| `maxmem` | int | Общая RAM, байт |
| `disk` | int | Использованный rootfs, байт |
| `maxdisk` | int | Общий объём rootfs, байт |
| `uptime` | int | Аптайм, секунд |
| `level` | str | Уровень поддержки |
| `ssl_fingerprint` | str | TLS-отпечаток |

**Пример:**
```yaml
{% set ep = env.PROXMOX_ENDPOINT %}
{% set tok = env.PROXMOX_TOKEN %}
{% set nodes = get_nodes_legacy(ep, tok) %}
node_time:
  {% for n in nodes %}
  - node: {{ n.node }}
    timezone: Europe/Moscow
  {% endfor %}
```

---

### `get_node_legacy(endpoint, api_token, node_name, insecure=False)`

**REST:** `GET /api2/json/nodes/{node_name}/status`

**Возвращает:** `dict`

| Поле | Тип | Описание |
|------|-----|----------|
| `node` | str | Имя узла |
| `status` | str | `online` \| `offline` |
| `cpu` | float | Загрузка CPU (0.0–1.0) |
| `cpuinfo` | dict | `{cpus, cores, sockets, mhz, model, ...}` |
| `memory` | dict | `{total, free, used}`, байт |
| `rootfs` | dict | `{total, free, used, avail}`, байт |
| `swap` | dict | `{total, free, used}`, байт |
| `uptime` | int | Аптайм, секунд |
| `loadavg` | list[str] | Средняя нагрузка: 1, 5, 15 мин |

**Пример:**
```yaml
{% set node = get_node_legacy(ep, tok, "pve") %}
# CPU: {{ node.cpuinfo.cpus }} / RAM: {{ node.memory.total }}
```

---

## Виртуальные машины

### `get_vms_legacy(endpoint, api_token, node_name, insecure=False)`

**REST:** `GET /api2/json/nodes/{node_name}/qemu`

**Возвращает:** `list[dict]`

| Поле | Тип | Описание |
|------|-----|----------|
| `vmid` | int | ID виртуальной машины |
| `name` | str | Имя VM |
| `status` | str | `running` \| `stopped` |
| `cpu` | float | Загрузка CPU (0.0–1.0) |
| `cpus` | int | Количество vCPU |
| `mem` | int | Использованная RAM, байт |
| `maxmem` | int | Выделенная RAM, байт |
| `disk` | int | Использованный диск, байт |
| `maxdisk` | int | Размер диска, байт |
| `uptime` | int | Аптайм, секунд |
| `template` | int | `1` = шаблон |
| `tags` | str | Теги через `;` |

**Пример:**
```yaml
{% set vms = get_vms_legacy(ep, tok, "pve") %}
{% set templates = vms | selectattr('template', 'eq', 1) | list %}
```

---

### `get_vm_legacy(endpoint, api_token, node_name, vm_id, insecure=False)`

**REST:** `GET /api2/json/nodes/{node_name}/qemu/{vm_id}/config`  
**Псевдонимы:** `get_vm`, `get_vm2_legacy`

**Возвращает:** `dict` (конфигурация VM)

| Поле | Тип | Описание |
|------|-----|----------|
| `name` | str | Имя VM |
| `cores` | int | Количество ядер |
| `sockets` | int | Количество сокетов |
| `memory` | int | RAM, МБ |
| `ostype` | str | Тип ОС: `l26`, `win11`, и др. |
| `boot` | str | Порядок загрузки |
| `template` | int | `1` = шаблон |
| `tags` | str | Теги через `;` |
| `description` | str | Описание |
| `net0`…`netN` | str | Конфигурация сетевых интерфейсов |
| `scsi0`…`scsiN` | str | Конфигурация SCSI-дисков |
| `agent` | str | Конфигурация QEMU Guest Agent |

**Пример:**
```yaml
{% set vm = get_vm_legacy(ep, tok, "pve", 100) %}
# VM: {{ vm.name }}, RAM: {{ vm.memory }} MB
```

---

## Контейнеры LXC

### `get_containers_legacy(endpoint, api_token, node_name, insecure=False)`

**REST:** `GET /api2/json/nodes/{node_name}/lxc`

**Возвращает:** `list[dict]`

| Поле | Тип | Описание |
|------|-----|----------|
| `vmid` | int | ID контейнера |
| `name` | str | Имя контейнера |
| `status` | str | `running` \| `stopped` |
| `cpu` | float | Загрузка CPU (0.0–1.0) |
| `cpus` | int | Количество vCPU |
| `mem` | int | Использованная RAM, байт |
| `maxmem` | int | Выделенная RAM, байт |
| `disk` | int | Использованный диск, байт |
| `maxdisk` | int | Размер диска, байт |
| `uptime` | int | Аптайм, секунд |
| `tags` | str | Теги через `;` |

---

### `get_container_legacy(endpoint, api_token, node_name, vm_id, insecure=False)`

**REST:** `GET /api2/json/nodes/{node_name}/lxc/{vm_id}/config`

**Возвращает:** `dict` (конфигурация контейнера)

| Поле | Тип | Описание |
|------|-----|----------|
| `hostname` | str | Имя хоста |
| `cores` | int | Количество ядер |
| `memory` | int | RAM, МБ |
| `swap` | int | Swap, МБ |
| `ostype` | str | Тип ОС: `debian`, `ubuntu`, и др. |
| `rootfs` | str | Конфигурация корневого диска |
| `net0`…`netN` | str | Конфигурация сетевых интерфейсов |
| `unprivileged` | int | `1` = непривилегированный контейнер |
| `tags` | str | Теги через `;` |
| `description` | str | Описание |

---

## Хранилища

### `get_datastores(endpoint, api_token, node_name, insecure=False)`

**REST:** `GET /api2/json/nodes/{node_name}/storage`  
**Псевдоним:** `get_datastores_legacy`

**Возвращает:** `list[dict]`

| Поле | Тип | Описание |
|------|-----|----------|
| `storage` | str | Имя хранилища |
| `type` | str | Тип: `dir`, `nfs`, `lvm`, `zfspool`, и др. |
| `content` | str | Поддерживаемые типы содержимого через `,` |
| `active` | int | `1` = активно |
| `enabled` | int | `1` = включено |
| `shared` | int | `1` = общее для всех узлов |
| `avail` | int | Доступно, байт |
| `total` | int | Всего, байт |
| `used` | int | Использовано, байт |
| `used_fraction` | float | Доля использования (0.0–1.0) |

**Пример:**
```yaml
{% set stores = get_datastores(ep, tok, "pve") %}
{% set local_lvm = stores | selectattr('storage', 'eq', 'local-lvm') | first %}
vms:
  - name: vm-test
    disks:
      - datastore: {{ local_lvm.storage }}
        size: 20
```

---

## Конфигурация узла

### `get_dns_legacy(endpoint, api_token, node_name, insecure=False)`

**REST:** `GET /api2/json/nodes/{node_name}/dns`

**Возвращает:** `dict`

| Поле | Тип | Описание |
|------|-----|----------|
| `search` | str | Домен поиска |
| `dns1` | str | Первичный DNS |
| `dns2` | str | Вторичный DNS (опционально) |
| `dns3` | str | Третичный DNS (опционально) |

---

### `get_hosts_legacy(endpoint, api_token, node_name, insecure=False)`

**REST:** `GET /api2/json/nodes/{node_name}/hosts`

**Возвращает:** `dict`

| Поле | Тип | Описание |
|------|-----|----------|
| `data` | str | Содержимое `/etc/hosts` |
| `digest` | str | SHA1-хеш файла |

---

### `get_time_legacy(endpoint, api_token, node_name, insecure=False)`

**REST:** `GET /api2/json/nodes/{node_name}/time`

**Возвращает:** `dict`

| Поле | Тип | Описание |
|------|-----|----------|
| `timezone` | str | Часовой пояс, например `Europe/Moscow` |
| `time` | int | Unix-время UTC |
| `localtime` | int | Локальное Unix-время |

---

## Файлы на storage

### `get_files(endpoint, api_token, node_name, datastore_id, insecure=False)`

**REST:** `GET /api2/json/nodes/{node_name}/storage/{datastore_id}/content`

**Возвращает:** `list[dict]`

| Поле | Тип | Описание |
|------|-----|----------|
| `volid` | str | Идентификатор тома, например `local:iso/ubuntu.iso` |
| `content` | str | Тип содержимого: `iso`, `images`, `vztmpl`, и др. |
| `format` | str | Формат: `raw`, `qcow2`, `iso`, и др. |
| `size` | int | Размер, байт |
| `ctime` | int | Время создания, Unix-timestamp |
| `vmid` | int | ID VM-владельца (опционально) |
| `notes` | str | Заметки (опционально) |

---

### `get_file(endpoint, api_token, node_name, datastore_id, file_id, insecure=False)`

**REST:** `GET /api2/json/nodes/{node_name}/storage/{datastore_id}/content/{file_id}`  
**Псевдоним:** `get_file_legacy`

Возвращает информацию об одном файле. Поля аналогичны `get_files`.

---

## HA (High Availability)

### `get_hagroups(endpoint, api_token, insecure=False)`

**REST:** `GET /api2/json/cluster/ha/groups`  
**Псевдоним:** `get_hagroups_legacy`

**Возвращает:** `list[dict]`

| Поле | Тип | Описание |
|------|-----|----------|
| `group` | str | Имя группы |
| `type` | str | Всегда `group` |
| `nodes` | str | Список узлов через `,` |
| `comment` | str | Комментарий (опционально) |

---

### `get_hagroup(endpoint, api_token, group, insecure=False)`

**REST:** `GET /api2/json/cluster/ha/groups/{group}`  
**Псевдоним:** `get_hagroup_legacy`

**Возвращает:** `dict`

| Поле | Тип | Описание |
|------|-----|----------|
| `group` | str | Имя группы |
| `nodes` | str | Список узлов через `,` с опциональными приоритетами |
| `restricted` | int | `1` = только разрешённые узлы |
| `nofailback` | int | `1` = не мигрировать обратно |
| `comment` | str | Комментарий (опционально) |

---

### `get_haresources(endpoint, api_token, insecure=False)`

**REST:** `GET /api2/json/cluster/ha/resources`  
**Псевдоним:** `get_haresources_legacy`

**Возвращает:** `list[dict]`

| Поле | Тип | Описание |
|------|-----|----------|
| `sid` | str | Service ID, например `vm:100` |
| `type` | str | `vm` \| `ct` |
| `state` | str | `started` \| `stopped` \| `ignored` \| `disabled` |
| `group` | str | HA-группа (опционально) |
| `max_restart` | int | Максимум рестартов |
| `max_relocate` | int | Максимум переносов |

---

### `get_haresource(endpoint, api_token, resource_id, insecure=False)`

**REST:** `GET /api2/json/cluster/ha/resources/{resource_id}`  
**Псевдоним:** `get_haresource_legacy`

Возвращает конфигурацию одного ресурса. Поля аналогичны `get_haresources`.

---

## Пулы

### `get_pools_legacy(endpoint, api_token, insecure=False)`

**REST:** `GET /api2/json/pools`

**Возвращает:** `list[dict]`

| Поле | Тип | Описание |
|------|-----|----------|
| `poolid` | str | Имя пула |
| `comment` | str | Комментарий (опционально) |

---

### `get_pool_legacy(endpoint, api_token, pool_id, insecure=False)`

**REST:** `GET /api2/json/pools/{pool_id}`

**Возвращает:** `dict`

| Поле | Тип | Описание |
|------|-----|----------|
| `poolid` | str | Имя пула |
| `comment` | str | Комментарий |
| `members` | list[dict] | Ресурсы пула: `{vmid, type, node, ...}` |

---

## RBAC

### `get_roles_legacy(endpoint, api_token, insecure=False)`

**REST:** `GET /api2/json/access/roles`

**Возвращает:** `list[dict]`

| Поле | Тип | Описание |
|------|-----|----------|
| `roleid` | str | Имя роли |
| `privs` | str | Привилегии через `,` |
| `special` | int | `1` = встроенная роль |

---

### `get_role_legacy(endpoint, api_token, role_id, insecure=False)`

**REST:** `GET /api2/json/access/roles/{role_id}`

**Возвращает:** `dict` — объект с полями-привилегиями, каждое `bool`.

---

### `get_groups_legacy(endpoint, api_token, insecure=False)`

**REST:** `GET /api2/json/access/groups`

**Возвращает:** `list[dict]`

| Поле | Тип | Описание |
|------|-----|----------|
| `groupid` | str | Имя группы |
| `comment` | str | Комментарий (опционально) |

---

### `get_group_legacy(endpoint, api_token, group_id, insecure=False)`

**REST:** `GET /api2/json/access/groups/{group_id}`

**Возвращает:** `dict`

| Поле | Тип | Описание |
|------|-----|----------|
| `groupid` | str | Имя группы |
| `users` | list[str] | Список пользователей |
| `comment` | str | Комментарий (опционально) |

---

### `get_users_legacy(endpoint, api_token, insecure=False)`

**REST:** `GET /api2/json/access/users`

**Возвращает:** `list[dict]`

| Поле | Тип | Описание |
|------|-----|----------|
| `userid` | str | Логин в формате `user@realm` |
| `enable` | int | `1` = включён |
| `comment` | str | Комментарий (опционально) |
| `email` | str | Email (опционально) |
| `expire` | int | Unix-timestamp истечения, `0` = бессрочно |
| `firstname` | str | Имя (опционально) |
| `lastname` | str | Фамилия (опционально) |
| `groups` | list[str] | Группы (опционально) |

---

### `get_user_legacy(endpoint, api_token, user_id, insecure=False)`

**REST:** `GET /api2/json/access/users/{user_id}`

Возвращает конфигурацию одного пользователя. Поля аналогичны `get_users_legacy`.

---

## Репликация

### `get_replications(endpoint, api_token, insecure=False)`

**REST:** `GET /api2/json/cluster/replication`  
**Псевдоним:** `get_replications_legacy`

**Возвращает:** `list[dict]`

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | str | ID задачи репликации |
| `type` | str | Тип: `zfslocal` |
| `source` | str | Узел-источник |
| `target` | str | Узел-назначение |
| `schedule` | str | Расписание в формате systemd calendar |
| `enabled` | int | `1` = включена |
| `comment` | str | Комментарий (опционально) |

---

### `get_replication(endpoint, api_token, id, insecure=False)`

**REST:** `GET /api2/json/cluster/replication/{id}`  
**Псевдоним:** `get_replication_legacy`

Возвращает конфигурацию одной задачи. Поля аналогичны `get_replications`.

---

## ACME

### `acme.get_accounts(endpoint, api_token, insecure=False)`

**REST:** `GET /api2/json/cluster/acme/account`

**Возвращает:** `list[dict]`

| Поле | Тип | Описание |
|------|-----|----------|
| `name` | str | Имя аккаунта |
| `url` | str | URL ACME-директории |

---

### `acme.get_account(endpoint, api_token, name, insecure=False)`

**REST:** `GET /api2/json/cluster/acme/account/{name}`

**Возвращает:** `dict`

| Поле | Тип | Описание |
|------|-----|----------|
| `account` | dict | `{contact: [...], createdAt, status}` |
| `directory` | str | URL ACME-директории |
| `tos` | str | URL условий использования |
| `location` | str | URL аккаунта |

---

### `acme.get_plugins(endpoint, api_token, insecure=False)`

**REST:** `GET /api2/json/cluster/acme/plugins`

**Возвращает:** `list[dict]`

| Поле | Тип | Описание |
|------|-----|----------|
| `plugin` | str | Имя плагина |
| `type` | str | `dns` \| `standalone` |
| `api` | str | DNS-провайдер (для `dns`-плагинов) |

---

### `acme.get_plugin(endpoint, api_token, plugin, insecure=False)`

**REST:** `GET /api2/json/cluster/acme/plugins/{plugin}`

Возвращает конфигурацию одного плагина. Поля аналогичны `acme.get_plugins`.

---

## APT

### `apt.get_repository(endpoint, api_token, node_name, insecure=False)`

**REST:** `GET /api2/json/nodes/{node_name}/apt/repositories`  
**Псевдоним:** `apt.standard.get_repository`

**Возвращает:** `dict`

| Поле | Тип | Описание |
|------|-----|----------|
| `files` | list[dict] | Файлы репозиториев; каждый содержит `{path, repositories: [...]}` |
| `errors` | list[dict] | Ошибки парсинга (если есть) |
| `infos` | list[dict] | Информационные сообщения |
| `digest` | str | SHA1-хеш конфигурации |

---

## Backup

### `backup.get_jobs(endpoint, api_token, insecure=False)`

**REST:** `GET /api2/json/cluster/backup`

**Возвращает:** `list[dict]`

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | str | ID задачи |
| `storage` | str | Хранилище для бэкапов |
| `schedule` | str | Расписание в формате systemd calendar |
| `enabled` | int | `1` = включена |
| `compress` | str | Алгоритм сжатия: `lzo`, `gzip`, `zstd` |
| `mode` | str | Режим: `snapshot`, `suspend`, `stop` |
| `node` | str | Узел (опционально, пусто = все узлы) |
| `vmid` | str | Список VM/CT через `,` (опционально) |
| `mailnotification` | str | Условие отправки писем |

---

## Hardware Mappings

### `hardware.get_mappings(endpoint, api_token, insecure=False)`

**REST:** `GET /api2/json/cluster/mapping`

**Возвращает:** `list[dict]`

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | str | Имя маппинга |
| `type` | str | `pci` \| `usb` |

---

### `hardware.mapping.get_pci(endpoint, api_token, name, insecure=False)`

**REST:** `GET /api2/json/cluster/mapping/pci/{name}`

**Возвращает:** `dict`

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | str | Имя маппинга |
| `description` | str | Описание (опционально) |
| `map` | list[dict] | Маппинг `{node, path, id, subsystem-id}` для каждого узла |

---

### `hardware.mapping.get_usb(endpoint, api_token, name, insecure=False)`

**REST:** `GET /api2/json/cluster/mapping/usb/{name}`

**Возвращает:** `dict`

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | str | Имя маппинга |
| `description` | str | Описание (опционально) |
| `map` | list[dict] | Маппинг `{node, path, id}` для каждого узла |

---

## Метрики

### `metrics.get_server(endpoint, api_token, name, insecure=False)`

**REST:** `GET /api2/json/cluster/metrics/server/{name}`

**Возвращает:** `dict`

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | str | Имя сервера метрик |
| `type` | str | `graphite` \| `influxdb` |
| `server` | str | Адрес сервера |
| `port` | int | Порт |
| `enabled` | int | `1` = включён |
| `mtu` | int | MTU (опционально) |
| `timeout` | int | Таймаут, секунд (опционально) |

---

## SDN

### `sdn.get_zones(endpoint, api_token, insecure=False)`

**REST:** `GET /api2/json/cluster/sdn/zones`

**Возвращает:** `list[dict]`

| Поле | Тип | Описание |
|------|-----|----------|
| `zone` | str | Имя зоны |
| `type` | str | `simple` \| `vlan` \| `vxlan` \| `evpn` \| `qinq` |
| `state` | str | Состояние |
| `nodes` | str | Список узлов через `,` (опционально) |
| `mtu` | int | MTU (опционально) |

---

### `sdn.get_vnets(endpoint, api_token, insecure=False)`

**REST:** `GET /api2/json/cluster/sdn/vnets`

**Возвращает:** `list[dict]`

| Поле | Тип | Описание |
|------|-----|----------|
| `vnet` | str | Имя vnet |
| `zone` | str | Родительская зона |
| `type` | str | Всегда `vnet` |
| `tag` | int | VLAN/VNI-тег (опционально) |
| `vlanaware` | int | `1` = VLAN-aware (опционально) |

---

### `sdn.get_vnet(endpoint, api_token, id, insecure=False)`

**REST:** `GET /api2/json/cluster/sdn/vnets/{id}`

Возвращает конфигурацию одной vnet. Поля аналогичны `sdn.get_vnets`.

---

### `sdn.get_subnet(endpoint, api_token, vnet, cidr, insecure=False)`

**REST:** `GET /api2/json/cluster/sdn/vnets/{vnet}/subnets/{cidr}`

`cidr` кодируется автоматически (например `10.0.0.0/24` → `10.0.0.0-24`).

**Возвращает:** `dict`

| Поле | Тип | Описание |
|------|-----|----------|
| `subnet` | str | ID подсети |
| `cidr` | str | CIDR, например `10.0.0.0/24` |
| `vnet` | str | Родительская vnet |
| `gateway` | str | Шлюз (опционально) |
| `snat` | int | `1` = SNAT включён (опционально) |

---

### `sdn.get_zone(endpoint, api_token, id, insecure=False)`

**REST:** `GET /api2/json/cluster/sdn/zones/{id}`

Возвращает конфигурацию одной зоны. Поля зависят от типа зоны.

**Псевдонимы:**

| Функция | Описание |
|---------|----------|
| `sdn.zone.get_evpn(ep, tok, id)` | EVPN-зона |
| `sdn.zone.get_simple(ep, tok, id)` | Simple-зона |
| `sdn.zone.get_vlan(ep, tok, id)` | VLAN-зона |
| `sdn.zone.get_vxlan(ep, tok, id)` | VXLAN-зона |
| `sdn.zone.get_qinq(ep, tok, id)` | QinQ-зона |

Все псевдонимы вызывают один и тот же REST-эндпоинт.

---

### `sdn.fabric.get_openfabric(endpoint, api_token, id, insecure=False)`

**REST:** `GET /api2/json/cluster/sdn/fabrics/{id}`  
**Псевдоним:** `sdn.fabric.get_ospf`

Возвращает конфигурацию SDN-фабрики.

---

### `sdn.fabric.node.get_openfabric(endpoint, api_token, fabric_id, node_id, insecure=False)`

**REST:** `GET /api2/json/cluster/sdn/fabrics/{fabric_id}/nodes/{node_id}`  
**Псевдоним:** `sdn.fabric.node.get_ospf`

Возвращает конфигурацию узла SDN-фабрики.
