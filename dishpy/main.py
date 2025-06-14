import sys
import os
import shutil
import argparse
from pathlib import Path
from . import __version__
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from .vexcom import run_vexcom
from .amalgamator import combine_project
import tomllib
import tomli_w
import textcase

console = Console()


class Project:
    def __init__(self, path: Path, name: str, slot: int):
        self.src = path / "src"
        self.main_file = path / "src" / "main.py"
        self.vex_dir = path / "src" / "vex"
        self.vex_init = path / "src" / "vex" / "__init__.py"
        self.out_dir = path / ".out"

        self.name = name
        self.slot = slot

        for i in [self.src, self.main_file, self.vex_dir, self.vex_init, self.out_dir]:
            if not i.exists():
                raise FileNotFoundError()

    @staticmethod
    def scaffold(path: Path | None = None, name: str | None = None, slot: int | None = None):
        if not path:
            path = Path.cwd()
        if not name:
            name = "My DishPy Project"
        if not slot:
            slot = 1
        with open(path / "dishpy.toml", "w") as f:
            f.write(f"[project]\nname = \"{name}\"\nslot = {slot}\n")
        src = path / "src"
        main_file = path / "src" / "main.py"
        vex_dir = path / "src" / "vex"
        vex_init = path / "src" / "vex" / "__init__.py"
        out_dir = path / ".out"

        name = name
        slot = slot

        for i in [src, vex_dir, out_dir]:
            if not i.exists():
                i.mkdir()

        script_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(script_dir, "resources", "template.py")
        vex_path = os.path.join(script_dir, "resources", "vex.py")

        # Copy template to src/main.py
        shutil.copy2(template_path, main_file)
        shutil.copy2(vex_path, vex_init)

    def mu(self, verbose=False):
        combine_project(self.main_file, self.out_dir / "main.py", verbose)
        run_vexcom("--name", self.name, "--slot", str(self.slot), "--write", "./.out/main.py")

class DishPy:
    """Contains metadata about the current project"""

    def __init__(self, path: Path):
        self.path = path
        config_path = self.path / "dishpy.toml"
        if not config_path.exists():
            raise FileNotFoundError("Cannot find 'dishpy.toml' in current directory")
        with open(config_path, "rb") as f:
            self.config = tomllib.load(f)
        if "project" in self.config and "name" in self.config["project"] and "slot" in self.config["project"]:
            try:
                self.instance = Project(self.path, self.config["project"]["name"], self.config["project"]["slot"])
            except FileNotFoundError:
                raise FileNotFoundError(f"Project '{self.config['project']['name']}' not found")
        else:
            raise FileNotFoundError("Malformed 'dishpy.toml' file")

class Cli:
    @staticmethod
    def show_help():
        """Display help information"""
        help_text = Text()
        help_text.append(f"dishpy {__version__}", style="bold magenta")
        help_text.append(" - VEX Competition Development Tool\n\n", style="white")
        help_text.append("Commands:\n", style="bold white")
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
    @staticmethod
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

    def __init__(self):
        self.console = console
        self.project = None

    def route(self):
        if len(sys.argv) <= 1 or sys.argv[1] in ["-h", "--help", "help"]:
            self.show_help()
            return
        parser = self.parse_args()
        try:
            args = parser.parse_args()
        except SystemExit:
            self.show_help()
            return
        if args.command == "create":
            path = (Path() / args.name)
            path.mkdir()
            console.print(
                f"✨ [green]Created and initialized project in[/green] [bold cyan]{path}/[/bold cyan]"
            )
            Project.scaffold(path, args.name, args.slot)
        elif args.command == "mu":
            try:
                instance = DishPy(Path())
                instance.instance.mu()
            except Exception as e:
                self.console.print(f"❌ [red]Error: {e}[/red]")
        elif args.command == "vexcom":
            run_vexcom(*args.args)
        else:
            self.show_help()

def main():
    """Main entry point"""
    cli = Cli()
    cli.route()


if __name__ == "__main__":
    main()
