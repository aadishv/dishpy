# DishPy

A Python development tool for VEX Competition robotics that combines multi-file Python projects into single scripts and uploads them to VEX V5 brains.

## Features

- **Project Management**: Initialize new VEX robotics projects with a structured template
- **Code Amalgamation**: Combine multi-file Python projects into single scripts with intelligent symbol prefixing
- **VEX Integration**: Built-in VEX library support and seamless upload to V5 brains
- **Cross-Platform**: Works on Linux (x64, ARM32, ARM64), macOS, and Windows

## Installation

todo!

## Quick Start

### 1. Initialize a New Project

```bash
dishpy init
```

This creates:
- `src/main.py` - Main robot code from template
- `src/vex/__init__.py` - VEX library for robot control. Do not touch this; it stubs the VEX API for better autocomplete and LSP support in code editors.
- `dishpy.json` - Project configuration
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
├── dishpy.json         # Project configuration
└── .out/              # Combined output
```

**Note that all competition functions, such as `autonomous` and `driver`, have to be in `main.py`.**


### 3. Build and Upload

```bash
dishpy mu
```

This command:
1. Combines all Python files in `src/` into a single script
2. Resolves imports and prevents naming conflicts with intelligent prefixing
3. Uploads the combined code to your VEX V5 brain

## Commands

### `dishpy init`
Initialize a new VEX robotics project with template files and project structure.

### `dishpy mu`
Build and upload your project:
- Combines multi-file project into single script
- Uploads to VEX V5 brain using project configuration
- Add `--verbose` flag for detailed output

### `dishpy vexcom [args...]`
Direct access to the underlying vexcom tool for advanced usage. Pass any vexcom arguments directly.

## Project Configuration

The `dishpy.json` file contains project settings:

```json
{
  "name": "My Robot Project",
  "slot": 1
}
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
