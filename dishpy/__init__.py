"""
DishPy - A Python development tool for VEX Competition robotics.

This package provides tools for developing VEX Competition robotics programs
in Python, including project initialization, code amalgamation, and upload
to VEX V5 brains.
"""

__version__ = "0.3.0"
__author__ = "Aadish V"
__email__ = "aadish@ohs.stanford.edu"

# Make main functions available at package level
from .main import main, init_project, create_project, mu_command, show_help

__all__ = [
    "main",
    "init_project",
    "create_project",
    "mu_command",
    "show_help",
    "__version__",
]
