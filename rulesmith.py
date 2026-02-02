#!/usr/bin/env python3
"""Direct entry point for Rulesmith CLI."""

import sys
from pathlib import Path

# Get the project root (directory containing this script)
project_root = Path(__file__).parent

# Remove any paths that might conflict (old cli directories)
paths_to_remove = [p for p in sys.path if "experiment/cli" in p and "rulesmith" not in p]
for p in paths_to_remove:
    sys.path.remove(p)

# Add the project root to Python path first
sys.path.insert(0, str(project_root))

# Now import and run
from cli.src.main import app

if __name__ == "__main__":
    app()
