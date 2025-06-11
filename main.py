import sys
import os
import shutil
import json
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from vexcom import run_vexcom
from amalgamator import combine_project

console = Console()

def init_project():
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

    # Create project.json in root directory
    project_config = {
        "name": "My DishPy Project",
        "slot": 1
    }
    project_json_path = "dishpy.json"
    with open(project_json_path, "w") as f:
        json.dump(project_config, f, indent=2)

    console.print(f"✨ [green]Initialized project with[/green] [bold cyan]{dest_path}[/bold cyan][green],[/green] [bold cyan]{vex_dest_path}[/bold cyan][green],[/green] [bold cyan]{project_json_path}[/bold cyan][green], and[/green] [bold cyan].out/[/bold cyan]")

def is_dishpy_project():
    """Check if current directory is a dishpy project"""
    return os.path.exists("dishpy.json") and os.path.exists("src/main.py")

def mu_command(verbose=False):
    """Handle mu command"""
    if is_dishpy_project():
        console.print("✅ [green]This is a DishPy project[/green]")

        # Read project configuration
        with open("dishpy.json", "r") as f:
            project_config = json.load(f)

        name = project_config.get("name", "My DishPy Project")
        slot = project_config.get("slot", 1)

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
    help_text.append("dishpy", style="bold magenta")
    help_text.append(" - VEX Competition Development Tool\n\n", style="white")
    help_text.append("Commands:\n", style="bold white")
    help_text.append("  init    ", style="bold cyan")
    help_text.append("Initialize a new project with src/main.py\n", style="white")
    help_text.append("  mu      ", style="bold cyan")
    help_text.append("Check if in a DishPy project\n", style="white")
    help_text.append("  vexcom  ", style="bold cyan")
    help_text.append("Run vexcom with specified arguments", style="white")

    panel = Panel(
        help_text,
        title="[bold blue]Help[/bold blue]",
        border_style="blue"
    )
    console.print(panel)

def main():
    if len(sys.argv) == 1:
        show_help()
    elif len(sys.argv) > 1 and sys.argv[1] == "init":
        init_project()
    elif len(sys.argv) > 1 and sys.argv[1] == "mu":
        verbose = "--verbose" in sys.argv
        mu_command(verbose)
    elif len(sys.argv) > 1 and sys.argv[1] == "vexcom":
        # Pass all arguments after "vexcom" to run_vexcom
        vexcom_args = sys.argv[2:]
        run_vexcom(*vexcom_args)

if __name__ == "__main__":
    main()
