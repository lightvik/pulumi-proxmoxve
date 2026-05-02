#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
WORKSPACE=/workspace
PROJECT_DIR=$WORKSPACE/sources/project
INV=$WORKSPACE/inventory.yaml

PULUMI_STACK=default

# ---------------------------------------------------------------------------
# Render inventory template (inventory.yaml.j2 → inventory.yaml)
# ---------------------------------------------------------------------------
if [[ -f "${INV}.j2" ]]; then
    python3 - "${INV}.j2" "$INV" <<'PYEOF'
import sys, os, yaml, jinja2
sys.path.insert(0, '/')
from render_helpers import JINJA2_GLOBALS

tmpl_path, out_path = sys.argv[1], sys.argv[2]
tmpl_dir  = os.path.dirname(os.path.abspath(tmpl_path))
tmpl_name = os.path.basename(tmpl_path)

jenv = jinja2.Environment(loader=jinja2.FileSystemLoader(tmpl_dir))

def load_yaml(path):
    full = path if os.path.isabs(path) else os.path.join(tmpl_dir, path)
    name = os.path.basename(full)
    if name.endswith('.j2'):
        content = jenv.get_template(name).render(env=os.environ)
    else:
        with open(full) as f:
            content = f.read()
    return yaml.safe_load(content)

jenv.globals['load_yaml'] = load_yaml
jenv.globals.update(JINJA2_GLOBALS)
open(out_path, 'w').write(jenv.get_template(tmpl_name).render(env=os.environ))
PYEOF
fi

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

# Выбирает стек $PULUMI_STACK, создаёт если не существует
ensure_stack() {
    pulumi stack select "$PULUMI_STACK" 2>/dev/null || pulumi stack init "$PULUMI_STACK"
}

# ---------------------------------------------------------------------------
# PROJECT STACK
# ---------------------------------------------------------------------------
hr "PROJECT STACK"

cd "$PROJECT_DIR"
ensure_stack

echo ""
echo "--- pulumi preview ---"
pulumi preview

confirm "Запустить pulumi up?" || { echo "Отменено."; exit 0; }
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
