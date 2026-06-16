<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="logo-dark.svg">
    <img src="logo-light.svg" alt="logo" width="660">
  </picture>
</div>

## Описание

Инструмент для управления инфраструктурой Proxmox VE через Pulumi (Python).

Конфигурация описывается в одном YAML-файле (`inventory.yaml.j2`), который поддерживает Jinja2-шаблонизацию — включая динамические запросы к Proxmox REST API прямо во время рендеринга. Весь процесс деплоя — интерактивный TUI-скрипт внутри Docker-контейнера.

## Что можно задеплоить

- **VM** — виртуальные машины (QEMU/KVM) с полным набором параметров
- **LXC** — контейнеры
- **Storage** — NFS, CIFS, LVM, LVM-thin, ZFS, PBS, Directory
- **Network** — Linux-бриджи и VLAN-интерфейсы на нодах
- **SDN** — зоны, vnets, подсети, fabrics (OpenFabric/OSPF)
- **Firewall** — правила, security groups, aliases, ipsets на уровне кластера/ноды/VM
- **RBAC** — роли, группы, пользователи, токены, ACL, LDAP/OpenID-реалмы
- **ACME** — DNS-плагины, аккаунты, сертификаты
- **HA** — группы, ресурсы, fencing-правила
- **Backup** — задания резервного копирования
- **Replication** — задания репликации
- **Downloads** — ISO и шаблоны контейнеров
- **Node config** — DNS, /etc/hosts, timezone
- **Cluster misc** — параметры кластера, HW mappings, metrics

## Как это работает

При старте контейнера `entrypoint.py`:

1. Рендерит `inventory.yaml.j2` → `inventory.yaml` (Jinja2 + Proxmox REST API)
2. Инициализирует Pulumi-стек (создаёт при первом запуске)
3. Показывает интерактивное меню действий:

```text
  Deploy        (preview → up)
  Preview only
  Refresh       (sync state с Proxmox)
  Destroy       (весь стек)
  Destroy target (выбрать ресурсы)
  Exit
```

**Destroy target** — показывает checkbox-список всех ресурсов стека, позволяет выбрать конкретные и удалить только их через `pulumi destroy --target`.

Все ресурсы управляются одним Pulumi-стеком (`sources/project/`).

## Структура проекта

```text
pulumi-proxmoxve/
  Dockerfile
  entrypoint.py            # TUI-оркестратор (меню: deploy / preview / refresh / destroy)
  render_helpers.py        # Jinja2-функции для запросов к Proxmox API
  inventory.yaml.j2        # ваш шаблон конфигурации (gitignore)
  inventory.yaml           # генерируется при запуске (gitignore)
  pulumi-state/            # Pulumi state backend (gitignore)
  sources/
    models.py              # Pydantic-модели всех параметров
    loader.py              # загрузка и валидация inventory.yaml
    vm.py                  # билдер VM
    lxc.py                 # билдер LXC
    cloud_init.py          # генератор cloud-init файла
    ssh_key.py             # генератор SSH-ключа
    storage.py             # билдер storage backends
    network.py             # билдер bridges и VLANs
    firewall.py            # билдер firewall
    rbac.py                # билдер RBAC
    acme.py                # билдер ACME
    ha.py                  # билдер HA
    backup.py              # билдер backup jobs
    replication.py         # билдер replication
    sdn.py                 # билдер SDN
    cluster_misc.py        # билдер cluster options, HW, metrics
    node_config.py         # билдер DNS / hosts / timezone
    pool.py                # билдер pools
    download.py            # билдер file downloads
    project/
      Pulumi.yaml
      __main__.py          # точка входа Pulumi
  docs/
    inventory.yaml.j2      # полный справочник всех параметров с примерами
    jinja_functions.md     # справочник Jinja2-функций для Proxmox API
  agents/
    architecture.md        # описание runtime pipeline
    inventory.md           # справочник модели Inventory
    builders.md            # паттерн добавления нового типа ресурса
    jinja2.md              # справочник render_helpers
```

## Предварительные требования

- Docker
- Proxmox VE с API-токеном

Создать API-токен в Proxmox: `Datacenter → Permissions → API Tokens`.  
Формат: `user@realm!token-id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

## Быстрый старт

### 1. Создать конфигурацию

Скопировать справочник как основу:

```bash
cp docs/inventory.yaml.j2 inventory.yaml.j2
```

Минимальный пример `inventory.yaml.j2`:

```yaml
provider:
  endpoint: {{ env.PROXMOX_ENDPOINT }}
  insecure: true
  api_token: {{ env.PROXMOX_TOKEN }}

vms:
  - name: myvm
    vmid: 101
    node: pve
    networks:
      - bridge: vmbr0
    disks:
      - size: 20
        datastore: local-lvm
```

Полный справочник всех параметров: [`docs/inventory.yaml.j2`](docs/inventory.yaml.j2)

### 2. Создать файл переменных окружения

```bash
cp .env.example .env
```

`.env`:

```dotenv
PROXMOX_ENDPOINT=https://<proxmox-ip>:8006
PROXMOX_TOKEN=root@pam!pulumi=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

> `.env` содержит секреты — добавьте его в `.gitignore`.

### 3. Запустить

```bash
docker run \
  --interactive \
  --tty \
  --rm \
  --volume "$(pwd):/workspace" \
  --env-file .env \
  ghcr.io/lightvik/pulumi-proxmoxve:latest
```

После старта откроется интерактивное меню — выберите действие стрелками, подтвердите Enter.

## Передача дополнительных файлов

Если `inventory.yaml.j2` импортирует qcow2-образы или другие файлы:

```bash
docker run \
  --interactive \
  --tty \
  --rm \
  --volume "$(pwd):/workspace" \
  --volume "/path/to/images:/workspace/images:ro" \
  --env-file .env \
  ghcr.io/lightvik/pulumi-proxmoxve:latest
```

## Переменные окружения

| Переменная | Описание |
| --- | --- |
| `PROXMOX_ENDPOINT` | URL Proxmox API, например `https://10.0.0.1:8006` |
| `PROXMOX_TOKEN` | API-токен в формате `user@realm!id=secret` |
| Любые другие | Доступны в шаблоне через `{{ env.VAR }}` |

## Jinja2 в inventory.yaml.j2

Шаблон рендерится при каждом старте контейнера. Доступны:

```yaml
# Переменная из окружения
api_token: {{ env.PROXMOX_TOKEN }}

# С fallback
node: {{ env.get('PROXMOX_NODE', 'pve') }}

# Импорт данных из другого файла (путь относительно inventory.yaml.j2)
{% set secrets = load_yaml('secrets.yaml') %}
api_token: {{ secrets.api_token }}

# Запрос к Proxmox API (все функции доступны без импорта)
{% set nodes = get_nodes_legacy(env.PROXMOX_ENDPOINT, env.PROXMOX_TOKEN) %}

# Условный блок
{% if env.get('ENABLE_SDN') == 'true' %}
sdn:
  ...
{% endif %}
```

Справочник всех доступных функций: [`docs/jinja_functions.md`](docs/jinja_functions.md)

## Pulumi state

State сохраняется в `pulumi-state/` внутри примонтированного тома — персистентен между запусками. При первом запуске стек создаётся автоматически.
