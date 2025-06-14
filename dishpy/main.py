import argparse
import os
import shutil
import sys

import tomli_w
import tomllib
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from . import __version__
from .amalgamator import combine_project
from .vexcom import run_vexcom

console = Console()


def init_project(name=None, slot=None):
    """Initialize a new project with src/main.py from template"""
    # Create src directory if it doesn't exist
    os.makedirs("src", exist_ok=True)

    # Create src/vex directory if it doesn't exist
    os.makedirs("src/vex", exist_ok=True)

    # Create .out directory if it doesn't exist
    os.makedirs(".out", exist_ok=True)

    # Get the path to the template and vex files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, "resources", "template.py")
    vex_path = os.path.join(script_dir, "resources", "vex.py")

    # Copy template to src/main.py
    dest_path = os.path.join("src", "main.py")
    shutil.copy2(template_path, dest_path)

    # Copy vex.py to src/vex/__init__.py
    vex_dest_path = os.path.join("src", "vex", "__init__.py")
    shutil.copy2(vex_path, vex_dest_path)

    # Create dishpy.toml in root directory
    project_config = {
        "project": {"name": name or "My DishPy Project", "slot": slot or 1}
    }
    project_toml_path = "dishpy.toml"
    with open(project_toml_path, "wb") as f:
        tomli_w.dump(project_config, f)

    console.print(
        f"✨ [green]Initialized project with[/green] [bold cyan]{dest_path}[/bold cyan][green],[/green] [bold cyan]{vex_dest_path}[/bold cyan][green],[/green] [bold cyan]{project_toml_path}[/bold cyan][green], and[/green] [bold cyan].out/[/bold cyan]"
    )


def create_project(name, slot=None):
    """Create a new project directory and initialize it"""
    if os.path.exists(name):
        console.print(f"❌ [red]Directory '{name}' already exists[/red]")
        return

    # Create the project directory
    os.makedirs(name)
    os.chdir(name)

    # Initialize the project
    init_project(name, slot)
    console.print(
        f"✨ [green]Created and initialized project in[/green] [bold cyan]{name}/[/bold cyan]"
    )


def is_dishpy_project():
    """Check if current directory is a dishpy project"""
    return os.path.exists("dishpy.toml") and os.path.exists("src/main.py")


def mu_command(verbose=False):
    """Handle mu command"""
    if is_dishpy_project():
        console.print("✅ [green]This is a DishPy project[/green]")

        # Read project configuration
        with open("dishpy.toml", "rb") as f:
            project_config = tomllib.load(f)

        project_section = project_config.get("project", {})
        name = project_section.get("name", "My DishPy Project")
        slot = project_section.get("slot", 1)

        # Create .out directory if it doesn't exist
        os.makedirs(".out", exist_ok=True)

        # Combine project files before running vexcom
        combine_project("src/main.py", ".out/main.py", verbose)

        # Run vexcom with project configuration
        run_vexcom("--name", name, "--slot", str(slot), "--write", "./.out/main.py")
    else:
        console.print("❌ [red]Not in a DishPy project directory[/red]")


def show_help():
    """Display help information"""
    help_text = Text()
    help_text.append(f"dishpy {__version__}", style="bold magenta")
    help_text.append(" - VEX Competition Development Tool\n\n", style="white")
    help_text.append("Commands:\n", style="bold white")
    help_text.append("  init     ", style="bold cyan")
    help_text.append("Initialize a new project in current directory\n", style="white")
    help_text.append("           ", style="bold cyan")
    help_text.append("Options: --name <name> --slot <slot>\n", style="dim white")
    help_text.append("  create   ", style="bold cyan")
    help_text.append("Create new directory and initialize project\n", style="white")
    help_text.append("           ", style="bold cyan")
    help_text.append(
        "Options: --name <name> (required) --slot <slot>\n", style="dim white"
    )
    help_text.append("  mu       ", style="bold cyan")
    help_text.append("Build and upload project to VEX V5 brain\n", style="white")
    help_text.append("           ", style="bold cyan")
    help_text.append("Options: --verbose\n", style="dim white")
    help_text.append("  vexcom   ", style="bold cyan")
    help_text.append(
        "Run vexcom with specified arguments (auto-installs if needed)", style="white"
    )

    panel = Panel(help_text, title="[bold blue]Help[/bold blue]", border_style="blue")
    console.print(panel)


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="DishPy - VEX Competition Development Tool", add_help=False
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Init command
    init_parser = subparsers.add_parser(
        "init", help="Initialize a new project in current directory"
    )
    init_parser.add_argument("--name", help="Project name")
    init_parser.add_argument("--slot", type=int, help="Project slot number")

    # Create command
    create_parser = subparsers.add_parser(
        "create", help="Create new directory and initialize project"
    )
    create_parser.add_argument("--name", required=True, help="Project name (required)")
    create_parser.add_argument("--slot", type=int, help="Project slot number")

    # Mu command
    mu_parser = subparsers.add_parser(
        "mu", help="Build and upload project to VEX V5 brain"
    )
    mu_parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose output"
    )

    # Vexcom command
    vexcom_parser = subparsers.add_parser(
        "vexcom", help="Run vexcom with specified arguments"
    )
    vexcom_parser.add_argument("args", nargs="*", help="Arguments to pass to vexcom")

    return parser


def main():
    if len(sys.argv) == 1:
        show_help()
        return

    parser = parse_args()

    # Handle help manually since we disabled add_help
    if sys.argv[1] in ["-h", "--help", "help"]:
        show_help()
        return

    try:
        args = parser.parse_args()
    except SystemExit:
        # argparse called sys.exit(), likely due to unknown command
        show_help()
        return

    if args.command == "init":
        init_project(args.name, args.slot)
    elif args.command == "create":
        create_project(args.name, args.slot)
    elif args.command == "mu":
        mu_command(args.verbose)
    elif args.command == "vexcom":
        run_vexcom(*args.args)
    else:
        show_help()


if __name__ == "__main__":
    main()
