# 1. Installation

Make sure you have [uv](https://github.com/astral-sh/uv) installed.

Add the following to your `.zshrc`, `.bashrc`, etc.:
```bash
export UV_INDEX_STRATEGY="unsafe-best-match"
export UV_EXTRA_INDEX_URL="https://test.pypi.org/simple/"
```
Open a new terminal to apply changes, and then run dishpy:
```bash
$ uv tool run dishpy
# or
$ uvx dishpy
# outputs something like
╭─────────────────────────────────────── Help ───────────────────────────────────────╮
│ dishpy 0.5.0 - VEX Competition Development Tool                                    │
│                                                                                    │
│ Commands:                                                                          │
│ create    Create new directory and initialize project                              │
│                 Options: --name <name> (required) --slot --package                 │
│ add       Add a previously registered package to a project                         │
│                 Options: package                                                   │
│ mu        Build and upload project to VEX V5 brain                                 │
│                 Options: --verbose                                                 │
│ vexcom    Run vexcom with specified arguments (auto-installs if needed)            │
│                 Options: args                                                      │
│ debug     debug DishPy CLI internals                                               │
│ list-pkgs List all available packages that have been registered with DishPy        │
│ register  Register a package with DishPy                                           │
│                 Options: package_path                                              │
│                                                                                    │
╰────────────────────────────────────────────────────────────────────────────────────╯
```
