# Ruff: A Beginner's Guide to the Python Linter & Formatter

> Ruff is an extremely fast Python linter and code formatter written in Rust. It replaces tools like Flake8, isort, pyupgrade, pydocstyle, and even Black — all in one package.

---

## Table of Contents

1. [Why Ruff?](#why-ruff)
2. [Installation](#installation)
3. [Basic Usage](#basic-usage)
4. [Configuration](#configuration)
5. [Rules & Rule Categories](#rules--rule-categories)
6. [Linting](#linting)
7. [Auto-fixing](#auto-fixing)
8. [Formatting](#formatting)
9. [Import Sorting](#import-sorting)
10. [Ignoring Rules](#ignoring-rules)
11. [Per-file Ignores](#per-file-ignores)
12. [Watching Files](#watching-files)
13. [CI/CD Integration](#cicd-integration)
14. [VS Code Extension](#vs-code-extension)
15. [Ruff vs Other Tools](#ruff-vs-other-tools)
16. [Quick Reference Cheat Sheet](#quick-reference-cheat-sheet)

---

## Why Ruff?

- **10–100× faster** than Flake8, pylint, and Black
- **Drop-in replacement** for many popular tools
- **Zero dependencies** — single binary, no virtual env pollution
- **pyproject.toml native** — one config file for everything
- **Auto-fix support** for hundreds of rules

---

## Installation

### Using pip

```bash
pip install ruff
```

### Using uv (recommended for speed)

```bash
uv add --dev ruff
```

### Using pipx (isolated global install)

```bash
# recommended with toll
uv tool install ruff

# pipx
pipx install ruff
```

### Using Homebrew (macOS/Linux)

```bash
brew install ruff
```

### Verify installation

```bash
ruff --version
# ruff 0.x.x
```

---

## Basic Usage

Given this example Python file `example.py`:

```python
import os
import sys
import json

x=1
y = 2+3

def greet(name):
    print("Hello, " + name )
    return None

class myClass:
    def __init__(self,x,y):
        self.x=x
        self.y =y
```

### Check for issues

```bash
ruff check example.py
```

**Output:**

```
example.py:1:8: F401 [*] `os` imported but unused
example.py:3:8: F401 [*] `json` imported but unused
example.py:5:2: E225 Missing whitespace around operator
example.py:12:7: N801 Class name `myClass` should use CapWords convention
Found 4 errors.
[*] 2 fixable with the `--fix` option.
```

### Check an entire directory

```bash
ruff check .
ruff check src/
ruff check src/ tests/
```

---

## Configuration

Ruff is configured via `pyproject.toml`, `ruff.toml`, or `.ruff.toml`. The recommended approach is `pyproject.toml`.

### pyproject.toml

```toml
[tool.ruff]
# Target Python version
target-version = "py311"

# Line length (default: 88)
line-length = 100

# Directories/files to exclude
exclude = [
    ".git",
    ".venv",
    "__pycache__",
    "migrations",
    "build",
    "dist",
]

# Allow unused variables when underscore-prefixed
[tool.ruff.lint]
dummy-variable-rgx = "^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"

# Enable rule sets
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # Pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "SIM", # flake8-simplify
]

# Disable specific rules
ignore = ["E501", "B008"]

[tool.ruff.format]
# Use double quotes (like Black)
quote-style = "double"
indent-style = "space"
line-ending = "auto"
```

### ruff.toml (standalone)

```toml
target-version = "py311"
line-length = 100

[lint]
select = ["E", "F", "I", "N", "UP"]
ignore = ["E501"]

[format]
quote-style = "double"
```

---

## Rules & Rule Categories

Ruff implements rules from many popular tools. Here is the full list of rule prefixes:

| Prefix | Source Tool            | Description                         |
|--------|------------------------|-------------------------------------|
| `E`    | pycodestyle            | PEP 8 style errors                  |
| `W`    | pycodestyle            | PEP 8 style warnings                |
| `F`    | Pyflakes               | Logical errors (unused imports etc) |
| `I`    | isort                  | Import sorting                      |
| `N`    | pep8-naming            | Naming conventions                  |
| `D`    | pydocstyle             | Docstring conventions               |
| `UP`   | pyupgrade              | Python version upgrade suggestions  |
| `B`    | flake8-bugbear         | Likely bugs and design problems     |
| `A`    | flake8-builtins        | Shadowing built-in names            |
| `C4`   | flake8-comprehensions  | Better list/dict/set comprehensions |
| `SIM`  | flake8-simplify        | Code simplification suggestions     |
| `ANN`  | flake8-annotations     | Type annotation enforcement         |
| `S`    | flake8-bandit          | Security checks                     |
| `T20`  | flake8-print           | Disallow print statements           |
| `PT`   | flake8-pytest-style    | Pytest best practices               |
| `RUF`  | Ruff-native            | Ruff's own rules                    |
| `ERA`  | eradicate              | Commented-out code                  |
| `PL`   | Pylint                 | Pylint-equivalent checks            |
| `TRY`  | tryceratops            | Exception handling patterns         |
| `PERF` | Perflint               | Performance anti-patterns           |
| `FURB` | refurb                 | Modern Python idioms                |

### List all available rules

```bash
ruff rule --all
```

### Get details on a specific rule

```bash
ruff rule F401
# Explains what F401 does, shows an example, and how to fix it
```

---

## Linting

### Check specific files

```bash
ruff check main.py utils.py
```

### Check with a specific rule set

```bash
ruff check --select E,F,I .
```

### Show source code alongside errors

```bash
ruff check --show-source example.py
```

**Output:**

```
example.py:1:8: F401 [*] `os` imported but unused
  |
1 | import os
  |        ^^ F401
  |
```

### Output as JSON (useful for tooling)

```bash
ruff check --output-format json example.py
```

### Count errors by rule

```bash
ruff check --statistics .
```

**Output:**

```
14     F401 [ *] `...` imported but unused
 8     E501 [  ] Line too long
 3     N806 [  ] Variable in function should be lowercase
```

### Check and exit with non-zero code on errors (CI use)

```bash
ruff check . --exit-non-zero-on-fix
```

---

## Auto-fixing

Ruff can automatically fix many issues. Rules marked with `[*]` in output are fixable.

### Fix all auto-fixable issues

```bash
ruff check --fix example.py
```

### Preview fixes without applying them

```bash
ruff check --diff example.py
```

**Output:**

```diff
--- example.py
+++ example.py
@@ -1,5 +1,4 @@
-import os
 import sys
-import json

 x = 1
```

### Fix only specific rules

```bash
ruff check --fix --select F401 .
```

### Enable unsafe fixes

Some fixes are marked "unsafe" because they may change behaviour. Opt in explicitly:

```bash
ruff check --fix --unsafe-fixes .
```

---

## Formatting

Ruff includes a Black-compatible formatter (since v0.1.2).

### Format a file

```bash
ruff format example.py
```

### Format an entire project

```bash
ruff format .
```

### Check formatting without changing files (CI use)

```bash
ruff format --check .
```

### Show a diff of what would change

```bash
ruff format --diff .
```

### Example: before and after formatting

**Before:**

```python
def calculate(x,y,z):
    result=x+y*z
    if result>100:
        return result
    else:
            return 0
```

**After `ruff format`:**

```python
def calculate(x, y, z):
    result = x + y * z
    if result > 100:
        return result
    else:
        return 0
```

---

## Import Sorting

Ruff replaces `isort`. Enable the `I` rule set:

```toml
[tool.ruff.lint]
select = ["I"]
```

```bash
ruff check --select I --fix .
```

### Configure import sections

```toml
[tool.ruff.lint.isort]
known-first-party = ["mypackage"]
known-third-party = ["requests", "pydantic"]
force-sort-within-sections = true
lines-after-imports = 2
```

**Before:**

```python
import os
import requests
import sys
from mypackage import utils
import json
```

**After:**

```python
import json
import os
import sys

import requests

from mypackage import utils
```

---

## Ignoring Rules

### Inline suppression — single line

```python
import os  # noqa: F401

x=1  # noqa: E225
```

### Inline suppression — all rules on a line

```python
import os  # noqa
```

### Suppress a block for formatting with comments

```python
# fmt: off
x =     1
# fmt: on
```

### File-level suppression (top of file)

```python
# ruff: noqa
```

---

## Per-file Ignores

Ignore specific rules for specific files or patterns:

```toml
[tool.ruff.lint.per-file-ignores]
# Ignore unused imports in __init__.py files
"__init__.py" = ["F401"]

# Allow print statements in scripts
"scripts/*.py" = ["T20"]

# Relax rules in tests
"tests/**/*.py" = ["S101", "ANN", "D"]
```

---

## Watching Files

You can pair it with `watchexec` or `entr`:

```bash
# Watch and re-lint on changes
ruff check --watch

# Watch and re-format on changes
ruff format --watch

# Using watchexec
watchexec -e py -- ruff check .

# Using entr
find . -name "*.py" | entr ruff check .
```

---

## CI/CD Integration

### GitHub Actions

```yaml
name: Lint

on: [push, pull_request]

jobs:
  ruff:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v3

      - name: Run Ruff linter
        run: uvx ruff check --output-format github .

      - name: Run Ruff formatter
        run: uvx ruff format --check .
```

The `--output-format github` flag annotates pull requests directly in the GitHub UI.

### Pre-commit hook

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.x.x # replace with lastest version
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

Install and run:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

---

## VS Code Extension

The **Ruff VS Code extension** integrates linting and formatting directly into the editor.

### Installation

1. Open VS Code
2. Press `Ctrl+Shift+X` (or `Cmd+Shift+X` on Mac) to open Extensions
3. Search for **"Ruff"** (publisher: `charliermarsh`)
4. Click **Install**

Or install via the command line:

```bash
code --install-extension astral-sh.ruff
```

### What it does

- Highlights lint errors and warnings inline as you type
- Shows quick-fix suggestions via the lightbulb menu (`Ctrl+.`)
- Formats your file on save (optional)
- Sorts imports on save (optional)

### VS Code settings (settings.json)

```jsonc
{
  // Use Ruff as the default formatter for Python
  "[python]": {
    "editor.defaultFormatter": "astral-sh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll.ruff": "explicit",
      "source.organizeImports.ruff": "explicit"
    }
  },

  // Optional: point to a specific ruff binary
  "ruff.path": ["/usr/local/bin/ruff"],

  // Optional: use ruff from the active virtual environment
  "ruff.interpreter": ["${workspaceFolder}/.venv/bin/python"],

  // Show ruff in the status bar
  "ruff.showNotifications": "always"
}
```

### Using Ruff in the VS Code command palette

Press `Ctrl+Shift+P` (or `Cmd+Shift+P`) and search for:

| Command                        | What it does                    |
|--------------------------------|---------------------------------|
| `Ruff: Fix all auto-fixable problems` | Runs `--fix` on current file |
| `Ruff: Format document`        | Formats the current file        |
| `Format Document`              | Uses Ruff if set as default     |
| `Organize Imports`             | Sorts imports via Ruff          |

### Quick fixes in editor

When Ruff detects an issue, a yellow/red squiggle appears. Click the lightbulb or press `Ctrl+.` to see available fixes:

```
⚡ Remove unused import `os`          [F401]
⚡ Add missing whitespace around `=`  [E225]
⚡ Rewrite as f-string                [UP032]
```

---

## Complete Working Example

Here is a realistic project setup:

**`pyproject.toml`**

```toml
[project]
name = "my-app"
version = "0.1.0"
requires-python = ">=3.11"

[tool.ruff]
target-version = "py311"
line-length = 100
exclude = [".venv", "migrations", "build"]

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # Pyflakes
    "I",    # isort
    "N",    # pep8-naming
    "UP",   # pyupgrade
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "SIM",  # flake8-simplify
    "RUF",  # Ruff-specific rules
]
ignore = [
    "E501",  # line too long (handled by formatter)
    "B008",  # do not perform function calls in default arguments
]
fixable = ["ALL"]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["S101"]
"__init__.py" = ["F401"]

[tool.ruff.lint.isort]
known-first-party = ["my_app"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

**Makefile targets**

```makefile
lint:
	ruff check .

format:
	ruff format .

fix:
	ruff check --fix .
	ruff format .

ci:
	ruff check --output-format github .
	ruff format --check .
```

---

## Ruff vs Other Tools

| Feature               | Ruff  | Flake8 | Black | isort | pylint |
|-----------------------|-------|--------|-------|-------|--------|
| Linting               | ✅    | ✅     | ❌    | ❌    | ✅     |
| Formatting            | ✅    | ❌     | ✅    | ❌    | ❌     |
| Import sorting        | ✅    | ❌     | ❌    | ✅    | ❌     |
| Auto-fix              | ✅    | limited| N/A   | ✅    | limited|
| Speed                 | 🚀🚀🚀 | 🚀    | 🚀    | 🚀    | 🐢    |
| Single binary         | ✅    | ❌     | ❌    | ❌    | ❌     |
| pyproject.toml native | ✅    | partial| ✅    | ✅    | partial|

---

## Quick Reference Cheat Sheet

```bash
# Install
pip install ruff

# Lint current directory
ruff check .

# Lint and auto-fix
ruff check --fix .

# Format all files
ruff format .

# Check formatting (no changes)
ruff format --check .

# See what would change (diff)
ruff check --diff .
ruff format --diff .

# Show source with errors
ruff check --show-source .

# Run only specific rules
ruff check --select F401,E501 .

# Ignore specific rules
ruff check --ignore E501 .

# Output stats summary
ruff check --statistics .

# Output JSON
ruff check --output-format json .

# GitHub Actions annotations
ruff check --output-format github .

# List all rules
ruff rule --all

# Explain a rule
ruff rule F401

# Show Ruff config being used
ruff check --show-settings .
```

---

*Generated with ❤️ for Python developers. For the latest rules and options, see the [official Ruff documentation](https://docs.astral.sh/ruff/).*
