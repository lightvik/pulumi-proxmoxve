#!/usr/bin/env python3
import json
import os
import sys
import subprocess

import yaml
import jinja2
import questionary
from rich.console import Console
from rich.panel import Panel
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
            with open(full, encoding="utf-8") as f:
                content = f.read()
        return yaml.safe_load(content)

    jenv.globals["load_yaml"] = load_yaml
    jenv.globals.update(JINJA2_GLOBALS)

    with console.status("[cyan]Рендеринг шаблона...", spinner="dots"):
        rendered = jenv.get_template(tmpl_name).render(env=os.environ)
        with open(INV, "w", encoding="utf-8") as f:
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
        check=False,
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
        check=False,
    )
    return (
        result.stdout.strip()
        if result.returncode == 0 and result.stdout.strip()
        else None
    )


def show_outputs():
    vm_ips = get_output("vm_ips")

    if not vm_ips:
        console.print("[dim]Нет доступных outputs.[/dim]")
        return

    console.print()
    console.rule("[bold green]Outputs")

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
    except (yaml.YAMLError, TypeError, AttributeError):
        console.print(
            Panel(Text(vm_ips), title="[bold]VM IP Адреса[/bold]", border_style="cyan")
        )


def action_deploy():
    console.print()
    console.rule("[bold blue]Preview")
    console.print()
    run(["pulumi", "preview"])

    console.print()
    if not questionary.confirm("Запустить pulumi up?", default=False).ask():
        console.print("[yellow]Отменено.[/yellow]")
        return

    console.print()
    console.rule("[bold blue]Deploy")
    console.print()
    run(["pulumi", "up", "--yes"])

    console.print()
    console.rule("[bold green]Деплой завершён")
    show_outputs()


def action_preview():
    console.print()
    console.rule("[bold blue]Preview")
    console.print()
    run(["pulumi", "preview"])


def action_refresh():
    console.print()
    console.rule("[bold blue]Refresh")
    console.print()
    run(["pulumi", "refresh", "--yes"])

    console.print()
    console.rule("[bold green]Refresh завершён")


def action_destroy():
    console.print()
    console.print(
        Panel(
            "[bold red]Будут удалены ВСЕ ресурсы стека![/bold red]",
            border_style="red",
        )
    )

    if not questionary.confirm("Вы уверены?", default=False).ask():
        console.print("[yellow]Отменено.[/yellow]")
        return

    confirm = questionary.text("Введите 'yes' для подтверждения:").ask()
    if confirm != "yes":
        console.print("[yellow]Отменено.[/yellow]")
        return

    console.print()
    console.rule("[bold red]Destroy")
    console.print()
    run(["pulumi", "destroy", "--yes"])

    console.print()
    console.rule("[bold green]Destroy завершён")


def action_destroy_target():
    console.print()
    console.rule("[bold yellow]Destroy Target")
    console.print()

    with console.status("[cyan]Получение списка ресурсов...", spinner="dots"):
        result = subprocess.run(
            ["pulumi", "stack", "export"],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            check=True,
        )

    state = json.loads(result.stdout)
    resources = state.get("deployment", {}).get("resources", [])

    choices = []
    for r in resources:
        rtype = r.get("type", "")
        if rtype.startswith("pulumi:"):
            continue
        urn = r.get("urn", "")
        name = urn.split("::")[-1] if "::" in urn else urn
        short_type = rtype.split("/")[-1] if "/" in rtype else rtype.split(":")[-1]
        choices.append(
            questionary.Choice(
                title=f"{name}  [{short_type}]",
                value=urn,
            )
        )

    if not choices:
        console.print("[yellow]Нет ресурсов для удаления.[/yellow]")
        return

    selected = questionary.checkbox(
        "Выберите ресурсы для удаления (пробел — выбрать, Enter — подтвердить):",
        choices=choices,
    ).ask()

    if not selected:
        console.print("[yellow]Ничего не выбрано. Отменено.[/yellow]")
        return

    console.print()
    console.print(
        Panel(
            "\n".join(f"[red]• {u.split('::')[-1]}[/red]" for u in selected),
            title="[bold red]Будут удалены:[/bold red]",
            border_style="red",
        )
    )

    if not questionary.confirm("Продолжить?", default=False).ask():
        console.print("[yellow]Отменено.[/yellow]")
        return

    cmd = ["pulumi", "destroy", "--yes"]
    for urn in selected:
        cmd += ["--target", urn]

    console.print()
    console.rule("[bold red]Destroy Target")
    console.print()
    run(cmd)

    console.print()
    console.rule("[bold green]Destroy завершён")


def main():
    console.print()
    console.rule(f"[bold blue]pulumi-proxmoxve {VERSION}")
    console.print()

    try:
        render_inventory()
        ensure_stack()

        while True:
            console.print()
            action = questionary.select(
                "Выберите действие:",
                choices=[
                    questionary.Choice("Deploy  (preview → up)", value="deploy"),
                    questionary.Choice("Preview only", value="preview"),
                    questionary.Choice(
                        "Refresh  (sync state с Proxmox)", value="refresh"
                    ),
                    questionary.Choice("Show outputs", value="outputs"),
                    questionary.Choice("Destroy        (весь стек)", value="destroy"),
                    questionary.Choice(
                        "Destroy target (выбрать ресурсы)", value="destroy_target"
                    ),
                    questionary.Choice("Exit", value="exit"),
                ],
            ).ask()

            if action == "deploy":
                action_deploy()
            elif action == "preview":
                action_preview()
            elif action == "refresh":
                action_refresh()
            elif action == "outputs":
                show_outputs()
            elif action == "destroy":
                action_destroy()
            elif action == "destroy_target":
                action_destroy_target()
            else:
                console.print("[dim]Выход.[/dim]")
                sys.exit(0)

    except subprocess.CalledProcessError as e:
        console.print()
        console.print(
            Panel(
                f"[red]Команда завершилась с кодом {e.returncode}[/red]\n"
                f"[dim]{' '.join(e.cmd)}[/dim]",
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
