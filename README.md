<p align="center">
  <img src="logo.svg" alt="Pulumi proxmoxve" height="150">
</p>

# pulumi-proxmoxve

Инструмент для развёртывания виртуальных машин на Proxmox VE через Pulumi (Python).

Конфигурация описывается в одном YAML-файле (`inventory.yaml.j2`), который поддерживает Jinja2-шаблонизацию. Весь процесс деплоя — интерактивный скрипт внутри Docker-контейнера.

## Как это работает

Деплой состоит из двух стеков:

1. **template** — создаёт «чистую» VM, запускает её (cloud-init настраивает систему), ждёт выключения, конвертирует в Proxmox template
2. **infra** — клонирует template нужное количество раз, настраивает сети, HA, пулы, SDN

Оркестрирует всё `entrypoint.sh`: последовательно запускает `pulumi preview` → запрашивает подтверждение → `pulumi up`, между стеками управляет VM через Proxmox API.

## Структура проекта

```text
pulumi-proxmoxve/
  Dockerfile
  entrypoint.sh
  inventory.yaml.j2       # шаблон конфигурации — редактировать здесь
  inventory.yaml          # генерируется при запуске (gitignore)
  pulumi-state/           # Pulumi state backend (gitignore)
  sources/
    models.py             # Pydantic-модели всех параметров
    loader.py             # загрузка inventory.yaml
    vm.py, cloud_init.py  # ...и остальные модули библиотеки
    infra/
      Pulumi.yaml
      __main__.py
    template/
      Pulumi.yaml
      __main__.py
  docs/
    inventory.yaml.j2     # полный справочник всех параметров с примерами
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

Обязательно заполнить в `inventory.yaml.j2`:

```yaml
provider:
  endpoint: https://<proxmox-ip>:8006
  insecure: true
  api_token: {{ env.PROXMOX_TOKEN }}   # или вписать напрямую

template:
  vmid: 9000
  iso_datastore: local
  iso_file: ubuntu-24.04-live-server-amd64.iso

defaults:
  node: pve
  ...

vms:
  - name: myvm
    vmid: 101
    networks:
      - zone: internal
        host: 10
```

### 2. Собрать образ

```bash
docker build -t pulumi-proxmoxve .
```

### 3. Запустить деплой

```bash
docker run -it \
  -v "$(pwd):/workspace" \
  -e PROXMOX_TOKEN="root@pam!pulumi=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" \
  pulumi-proxmoxve
```

Скрипт интерактивный — на каждом шаге спрашивает подтверждение перед выполнением.

## Переменные окружения

| Переменная        | Описание                                     |
|-------------------|----------------------------------------------|
| `PROXMOX_TOKEN`   | API-токен Proxmox (если используется в .j2)  |
| `PROXMOX_NODE`    | Имя ноды (если используется в .j2)           |
| Любые другие      | Доступны в шаблоне через `{{ env.VAR }}`     |

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

# Условный блок
{% if env.get('ENABLE_SDN') == 'true' %}
sdn:
  ...
{% endif %}
```

Полный справочник параметров: [`docs/inventory.yaml.j2`](docs/inventory.yaml.j2)

## Pulumi state

State сохраняется в `pulumi-state/` внутри примонтированного тома — персистентен между запусками контейнера. При первом запуске создаётся автоматически.
