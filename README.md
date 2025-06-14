# DishPy

A Python development tool for VEX Competition robotics that combines multi-file Python projects into single scripts and uploads them to VEX V5 brains.

## Roadmap

**Feature parity w/ VEX VSC extension**

 - [x] Bindings to vexcom
 - [x] Project initialization CLI
 - [x] Better documentation for using vexcom's common functions
 - [ ] VEXcom wrappers for ease-of-use
 - [ ] templates

**Core premise**

 - [x] Script amalgamation through AST parsing
 - [ ] Library creation functionality
 - [ ] Library installation functionality

**Future-leaning**

 - [ ] Simulation API
 - [ ] VSCode extension

## Why/when should I use DishPy over X?

* PROS/VEXcode text -> you don't like C++
* vexide -> you don't like Rust
* VEXcode blocks -> you're a grown up /j
* VEXcode Python -> you want multifile support, an editor other than VEXcode/VSCode, libraries (coming soon!), and a CLI

Note that, unlike PROS & vexide, DishPy is not a *from-scratch* rewrite that does scheduling and everything (as an eight grader I am physically unable to make such a thing). Instead, it uses the exact same Python VM as VEXcode and the VScode extension and uploads code in the exact same way and binds to the same SDK -- the only difference is that the DX of DishPy is wayyy better.

## Should you use DishPy?

Unfortunately, the answer right now is **probably not** if you are a competition team. I cannot confirm I will be available to debug or maintain this at all times, so keep that in mind.

If you do want to use this in competition, make sure to read the amalgamated files before running the programs to make sure nothing was lost in translation.

If you want to make this better, feel free to

1. Contribute and file a PR. The entire repository is open-source (that's probably how you are reading this :P)
2. Fork it! This is MIT licensed so you can do whatever you want
3. Play with it, report errors, and ping me in VTOW about them.


## Features

- **Project Management**: Initialize new VEX robotics projects with a structured template
- **Code Amalgamation**: Combine multi-file Python projects into single scripts with intelligent symbol prefixing
- **VEX Integration**: Built-in VEX library support and seamless upload to V5 brains
- **Cross-Platform**: Works on Linux (x64, ARM32, ARM64), macOS, and Windows

## Installation

Make sure you have [uv](https://github.com/astral-sh/uv) installed.

Add the following to your `.zshrc`, `.bashrc`, etc.:
```bash
export UV_INDEX_STRATEGY="unsafe-best-match"
export UV_EXTRA_INDEX_URL="https://test.pypi.org/simple/"
```
Open a new terminal to apply changes, and then run dishpy:
```bash
uv tool run dishpy
# or
uvx dishpy
```

## Quick Start

### 1. Initialize a New Project

```bash
# Create new directory and initialize project (required: --name)
uvx dishpy create --name "awesome-robot"

# Create with custom slot
uvx dishpy create --name "competition-bot" --slot 2
```

This creates:
- `src/main.py` - Main robot code from template
- `src/vex/__init__.py` - VEX library for robot control. Do not touch this; it stubs the VEX API for better autocomplete and LSP support in code editors.
- `dishpy.toml` - Project configuration
- `.out/` - Output directory for combined code

### 2. Develop Your Robot Code

Edit `src/main.py` and create additional modules in the `src/` directory. You can import and use modules freely - dishpy will handle combining them into a single file.

Example project structure:
```
my-robot/
├── src/
│   ├── main.py          # Main robot code
│   ├── autonomous.py    # Autonomous routines
│   ├── driver.py        # Driver control functions
│   └── vex/            # VEX library
│       └── __init__.py
├── dishpy.toml         # Project configuration
└── .out/              # Combined output
```

**Note that all competition functions, such as `autonomous` and `driver`, have to be in `main.py`.**


### 3. Build and Upload

```bash
uvx dishpy mu
```

This command:
1. Combines all Python files in `src/` into a single script
2. Resolves imports and prevents naming conflicts with intelligent prefixing
3. Uploads the combined code to your VEX V5 brain

## Commands

### Commands

#### `dishpy create`
Create a new project directory and initialize it with template files.

**Options:**
- `--name <name>` - Project name and directory name (**required**)
- `--slot <slot>` - Set program slot number (optional, defaults to 1)

**Examples:**
```bash
uvx dishpy create --name "my-robot"                # Creates my-robot/ directory
uvx dishpy create --name "competition-bot" --slot 2 # Custom slot
```

#### `dishpy mu`
Build and upload your project to a VEX V5 brain:
- Combines multi-file project into single script
- Uploads to VEX V5 brain using project configuration

**Options:**
- `--verbose` - Enable detailed output during build and upload

**Examples:**
```bash
uvx dishpy mu              # Standard build and upload
uvx dishpy mu --verbose    # Detailed output
```

#### `dishpy vexcom [args...]`
Direct access to the underlying vexcom tool for advanced usage. Pass any vexcom arguments directly.

**Examples:**
```bash
uvx dishpy vexcom --flag1 arg1 --etc
```

## Project Configuration

The `dishpy.toml` file contains project settings:

```toml
[project]
name = "test"
slot = 1
```

- `name`: Display name for your robot program
- `slot`: Program slot on the V5 brain (1-8)

## Code Amalgamation

DishPy's amalgamator intelligently combines multiple Python files into a single script by:

1. **Dependency Analysis**: Scans your project to understand import relationships
2. **Symbol Prefixing**: Prevents naming conflicts by prefixing symbols from different files
3. **Import Resolution**: Resolves local imports and preserves external library imports
4. **Topological Sorting**: Orders files correctly based on dependencies

### Example Usage

```python
from vex import *

# Create motor and sensor objects
left_motor = Motor(Ports.PORT1)
right_motor = Motor(Ports.PORT2)
controller = Controller()

# Drive robot
def drive():
    left_motor.spin(FORWARD, controller.axis1.position(), PERCENT)
    right_motor.spin(FORWARD, controller.axis2.position(), PERCENT)
```

## Platform Support

DishPy includes pre-compiled vexcom binaries for:
- Linux x64
- Linux ARM32 (Raspberry Pi)
- Linux ARM64 (Raspberry Pi 4+)
- macOS
- Windows 32-bit

## Requirements

- Python 3.12+
- VEX V5 Brain with USB connection

## Contributing

DishPy is designed to streamline VEX Competition robotics development in Python. Contributions are welcome for:
- Additional VEX library features
- Code amalgamation improvements
- Cross-platform compatibility
- Documentation and examples

## License

This project is licensed under the MIT License.

## Changelog

**v0.4**

* This is a **ground-up** rewrite of the entire DishPy CLI to now be significantly smaller and simpler. (It isn't vibe-coded anymore!)
* There are now slightly less debug messages which will hopefully be less annoying.
* We have removed `dishpy init` in favor of the more commonly used `dishpy create`.
* All of these changes go a long way towards having ✨libraries✨ in the near future!

**v0.3**

* Added a breaking bug that affected all users on v0.2.2. In the port to vexcom downloading, I accidentally deleted the vex.py resource. This will not affect creating or uploading projects, but will throw an error with running `dishpy init` or `dishpy create`. Fixed by adding back the file.
* Made docs look more modern! Plus, updated the home page with all of the new tidbits we have here.

**v0.2.2**

* Created a changelog!
* Instead of bundling the VEXcom executable with the repository, we now extract it from the VSCode extension. This better accomodates VEX licensing, although it does slightly worsen the UX as the CLI takes a few minutes to install on first VEXcom call.
* Vastly improved [documentation](https://aadishv.github.io/dishpy)! Hopefully I'll start writing topical tutorials as well soon.


## Credits

* Lewis | vexide (reverse-engineering vexcom calls)
* andrew | 781X (digging thru extension code w/ me)
* Aadish | 3151A (me)
* Chroma | 3332A | 3151A (inspiration)
* Gemini 2.5 Pro (LLM -- first run)
* Claude 4 Sonnet (LLM -- agentic tasks)
