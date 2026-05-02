#!/usr/bin/env python3
import os
import sys
import subprocess

import yaml
import jinja2
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.text import Text
from rich.table import Table
from rich import box

sys.path.insert(0, "/")
from render_helpers import JINJA2_GLOBALS

WORKSPACE = "/workspace"
PROJECT_DIR = f"{WORKSPACE}/sources/project"
INV = f"{WORKSPACE}/inventory.yaml"
PULUMI_STACK = "stack"

_pulumi_ver = os.environ.get("PULUMI_VERSION", "")
_proxmox_ver = os.environ.get("PROXMOXVE_VERSION", "")
_project_ver = os.environ.get("PROJECT_VERSION", "")
VERSION = f"{_pulumi_ver}-{_proxmox_ver}-v{_project_ver}" if _project_ver else "dev"

console = Console()


def render_inventory():
    tmpl_path = f"{INV}.j2"
    if not os.path.exists(tmpl_path):
        return

    console.rule("[bold blue]Рендеринг inventory")

    tmpl_dir = os.path.dirname(os.path.abspath(tmpl_path))
    tmpl_name = os.path.basename(tmpl_path)

    jenv = jinja2.Environment(loader=jinja2.FileSystemLoader(tmpl_dir))

    def load_yaml(path):
        full = path if os.path.isabs(path) else os.path.join(tmpl_dir, path)
        name = os.path.basename(full)
        if name.endswith(".j2"):
            content = jenv.get_template(name).render(env=os.environ)
        else:
            with open(full) as f:
                content = f.read()
        return yaml.safe_load(content)

    jenv.globals["load_yaml"] = load_yaml
    jenv.globals.update(JINJA2_GLOBALS)

    with console.status("[cyan]Рендеринг шаблона...", spinner="dots"):
        rendered = jenv.get_template(tmpl_name).render(env=os.environ)
        with open(INV, "w") as f:
            f.write(rendered)

    console.print(f"[green]✓[/green] inventory.yaml → [dim]{INV}[/dim]")


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=PROJECT_DIR, check=True, **kwargs)


def ensure_stack():
    os.makedirs(f"{WORKSPACE}/pulumi-state", exist_ok=True)
    result = subprocess.run(
        ["pulumi", "stack", "select", PULUMI_STACK],
        cwd=PROJECT_DIR,
        capture_output=True,
    )
    if result.returncode != 0:
        subprocess.run(
            ["pulumi", "stack", "init", PULUMI_STACK],
            cwd=PROJECT_DIR,
            capture_output=True,
            check=True,
        )


def get_output(name: str) -> str | None:
    result = subprocess.run(
        ["pulumi", "stack", "output", name, "--show-secrets"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
    )
    return (
        result.stdout.strip()
        if result.returncode == 0 and result.stdout.strip()
        else None
    )


def show_outputs():
    vm_ips = get_output("vm_ips")

    if not vm_ips:
        return

    console.print()
    console.rule("[bold green]Outputs")

    if vm_ips:
        try:
            ips = yaml.safe_load(vm_ips)
            if isinstance(ips, dict):
                table = Table(box=box.ROUNDED, border_style="cyan", show_header=True)
                table.add_column("VM", style="bold cyan")
                table.add_column("IP", style="white")
                for vm, ip in ips.items():
                    table.add_row(str(vm), str(ip))
                console.print(
                    Panel(table, title="[bold]VM IP Адреса[/bold]", border_style="cyan")
                )
            else:
                console.print(
                    Panel(
                        Text(str(vm_ips)),
                        title="[bold]VM IP Адреса[/bold]",
                        border_style="cyan",
                    )
                )
        except Exception:
            console.print(
                Panel(
                    Text(vm_ips), title="[bold]VM IP Адреса[/bold]", border_style="cyan"
                )
            )


def main():
    console.print()
    console.rule(f"[bold blue]pulumi-proxmoxve {VERSION}")
    console.print()

    try:
        render_inventory()
        ensure_stack()

        console.print()
        console.rule("[bold blue]Preview")
        console.print()
        run(["pulumi", "preview"])

        console.print()
        if not Confirm.ask(
            "[bold yellow]Запустить pulumi up?[/bold yellow]", default=False
        ):
            console.print("[red]Отменено.[/red]")
            sys.exit(0)

        console.print()
        console.rule("[bold blue]Deploy")
        console.print()
        run(["pulumi", "up", "--yes"])

        console.print()
        console.rule("[bold green]Деплой завершён")
        show_outputs()

    except subprocess.CalledProcessError as e:
        console.print()
        console.print(
            Panel(
                f"[red]Команда завершилась с кодом {e.returncode}[/red]\n[dim]{' '.join(e.cmd)}[/dim]",
                title="[bold red]Ошибка[/bold red]",
                border_style="red",
            )
        )
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        console.print("\n[yellow]Прервано пользователем.[/yellow]")
        sys.exit(1)


if __name__ == "__main__":
    main()
