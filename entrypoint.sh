#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
WORKSPACE=/workspace
TEMPLATE_DIR=$WORKSPACE/sources/template
INFRA_DIR=$WORKSPACE/sources/infra
INV=$WORKSPACE/inventory.yaml

PULUMI_STACK=default

# ---------------------------------------------------------------------------
# Render inventory template (inventory.yaml.j2 → inventory.yaml)
# ---------------------------------------------------------------------------
if [[ -f "${INV}.j2" ]]; then
    python3 - "${INV}.j2" "$INV" <<'PYEOF'
import sys, os, yaml, jinja2

tmpl_path, out_path = sys.argv[1], sys.argv[2]
tmpl_dir  = os.path.dirname(os.path.abspath(tmpl_path))
tmpl_name = os.path.basename(tmpl_path)

def load_yaml(path):
    full = path if os.path.isabs(path) else os.path.join(tmpl_dir, path)
    with open(full) as f:
        return yaml.safe_load(f)

jenv = jinja2.Environment(loader=jinja2.FileSystemLoader(tmpl_dir))
jenv.globals['load_yaml'] = load_yaml
open(out_path, 'w').write(jenv.get_template(tmpl_name).render(env=os.environ))
PYEOF
fi

# ---------------------------------------------------------------------------
# Read values from inventory.yaml
# ---------------------------------------------------------------------------
_inv() {
    python3 -c "import yaml; d=yaml.safe_load(open('$INV')); print($1)"
}

ENDPOINT=$(_inv "d['provider']['endpoint']")
API_TOKEN=$(_inv "d['provider']['api_token']")
DEFAULT_NODE=$(_inv "d['defaults']['node']")
TEMPLATE_VMID=$(_inv "d['template']['vmid']")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
confirm() {
    local ans
    echo ""
    read -r -p ">>> $1 [y/N] " ans
    [[ "${ans,,}" =~ ^y$ ]]
}

hr() {
    echo ""
    echo "=========================================="
    echo "  $1"
    echo "=========================================="
}

# Proxmox API call: proxmox_api GET|POST /path
proxmox_api() {
    local method=$1
    local path=$2
    curl -sf -k -X "$method" \
        -H "Authorization: PVEAPIToken=$API_TOKEN" \
        "$ENDPOINT/api2/json$path"
}

# Выбирает стек $PULUMI_STACK, создаёт если не существует
ensure_stack() {
    pulumi stack select "$PULUMI_STACK" 2>/dev/null || pulumi stack init "$PULUMI_STACK"
}

# ---------------------------------------------------------------------------
# TEMPLATE STACK
# ---------------------------------------------------------------------------
hr "TEMPLATE STACK"

cd "$TEMPLATE_DIR"
ensure_stack

echo ""
echo "--- pulumi preview ---"
pulumi preview

confirm "Запустить pulumi up для template стека?" || { echo "Отменено."; exit 0; }
pulumi up --yes

# Получаем ноду из outputs
TEMPLATE_NODE=$(pulumi stack output template_node 2>/dev/null || echo "$DEFAULT_NODE")

echo ""
echo "VM VMID=$TEMPLATE_VMID создана на ноде '$TEMPLATE_NODE'."

# ---------------------------------------------------------------------------
# Запуск VM
# ---------------------------------------------------------------------------
confirm "Запустить template VM (VMID=$TEMPLATE_VMID)?" || { echo "Отменено."; exit 0; }

echo "Запускаем VM..."
proxmox_api POST "/nodes/$TEMPLATE_NODE/qemu/$TEMPLATE_VMID/status/start" > /dev/null
echo "VM запущена. Ожидаем выключения (cloud-init завершится и выключит VM)..."

# Polling статуса
while true; do
    vm_status=$(proxmox_api GET "/nodes/$TEMPLATE_NODE/qemu/$TEMPLATE_VMID/status/current" \
        | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['status'])" 2>/dev/null \
        || echo "unknown")
    printf "\r  Статус VM: %-12s" "$vm_status"
    if [[ "$vm_status" == "stopped" ]]; then
        echo ""
        break
    fi
    sleep 10
done

echo "VM остановлена."

# ---------------------------------------------------------------------------
# Конвертация в template
# ---------------------------------------------------------------------------
confirm "Конвертировать VM $TEMPLATE_VMID в Proxmox template?" || { echo "Отменено."; exit 0; }

echo "Конвертируем в template..."
proxmox_api POST "/nodes/$TEMPLATE_NODE/qemu/$TEMPLATE_VMID/template" > /dev/null
echo "VM конвертирована в template."

# ---------------------------------------------------------------------------
# INFRA STACK
# ---------------------------------------------------------------------------
hr "INFRA STACK"

cd "$INFRA_DIR"
ensure_stack

echo ""
echo "--- pulumi preview ---"
pulumi preview

confirm "Запустить pulumi up для infra стека?" || { echo "Отменено."; exit 0; }
pulumi up --yes

# ---------------------------------------------------------------------------
hr "ДЕПЛОЙ ЗАВЕРШЁН"
echo ""
echo "SSH ключ:"
pulumi stack output ssh_private_key --show-secrets 2>/dev/null || true
echo ""
echo "IP адреса VM:"
pulumi stack output vm_ips 2>/dev/null || true
echo ""
