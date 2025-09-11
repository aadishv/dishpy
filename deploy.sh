#!/bin/bash
set -e
rm -rf dist/ build/ *.egg-info
uv build
uv run twine check dist/*
uv run twine upload dist/*
