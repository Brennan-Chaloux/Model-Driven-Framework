# Repo Split Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Split the monorepo into `mdf-simulator` (standalone library) and `mdf-server` (thin FastMCP adapter), linked via git submodule.

**Architecture:** All schema, tools, pycca, and engine code moves to `mdf-simulator` as a flat-layout Python package. `mdf-server` becomes a thin FastMCP wrapper that imports from the submodule. The submodule is mounted at `mdf-sim/` inside mdf-server and installed as an editable path dependency via uv.

**Tech Stack:** Python 3.11+, uv, hatchling (build backend), FastMCP 3.1.0, pytest

---

**Paths used throughout this plan:**
- `REPO` = `C:/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework`
- `SIM` = `C:/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator`
- `BACKUP` = `C:/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework-backup`

---

### Task 1: Initialize mdf-simulator directory structure

**Files:**
- Create directories in `SIM`

**Step 1: Create all package and support directories**

```bash
cd /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator
mkdir -p schema pycca tools engine cli tests docs .planning/phases .planning/research
```

**Step 2: Create top-level __init__.py files for each package**

Create `SIM/schema/__init__.py` — empty file.
Create `SIM/pycca/__init__.py` — empty file.
Create `SIM/tools/__init__.py` — empty file.
Create `SIM/engine/__init__.py` — empty file.
Create `SIM/cli/__init__.py` — empty file.

**Step 3: Verify structure**

```bash
find /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator -type f | sort
```

Expected: the 5 `__init__.py` files listed, directories visible.

---

### Task 2: Copy schema and pycca source files

**Files:**
- Copy: `REPO/mdf-server/mdf_server/schema/yaml_schema.py` → `SIM/schema/yaml_schema.py`
- Copy: `REPO/mdf-server/mdf_server/schema/drawio_schema.py` → `SIM/schema/drawio_schema.py`
- Copy: `REPO/mdf-server/mdf_server/pycca/__init__.py` → `SIM/pycca/__init__.py` (overwrites empty)

**Step 1: Copy the files**

```bash
cp /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-server/mdf_server/schema/yaml_schema.py \
   /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/schema/yaml_schema.py

cp /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-server/mdf_server/schema/drawio_schema.py \
   /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/schema/drawio_schema.py

cp /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-server/mdf_server/pycca/__init__.py \
   /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/pycca/__init__.py
```

**Step 2: Verify no internal mdf_server imports exist in schema files**

```bash
grep -r "mdf_server" /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/schema/ \
                     /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/pycca/
```

Expected: no output (schema files only use stdlib and pydantic).

---

### Task 3: Copy tools source files + fix internal imports

**Files:**
- Copy: `REPO/mdf-server/mdf_server/tools/model_io.py` → `SIM/tools/model_io.py`
- Copy: `REPO/mdf-server/mdf_server/tools/validation.py` → `SIM/tools/validation.py`
- Copy: `REPO/mdf-server/mdf_server/tools/drawio.py` → `SIM/tools/drawio.py`
- Copy: `REPO/mdf-server/mdf_server/tools/simulation.py` → `SIM/tools/simulation.py`

**Step 1: Copy the tools files**

```bash
cp /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-server/mdf_server/tools/model_io.py \
   /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/tools/model_io.py

cp /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-server/mdf_server/tools/validation.py \
   /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/tools/validation.py

cp /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-server/mdf_server/tools/drawio.py \
   /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/tools/drawio.py

cp /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-server/mdf_server/tools/simulation.py \
   /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/tools/simulation.py
```

**Step 2: Check for mdf_server imports that need updating**

```bash
grep -n "mdf_server" /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/tools/*.py
```

Expected output:
```
tools/model_io.py:9:from mdf_server.schema.yaml_schema import ClassDiagramFile
```

**Step 3: Fix the import in tools/model_io.py**

In `SIM/tools/model_io.py`, change line 9:

```python
# Before:
from mdf_server.schema.yaml_schema import ClassDiagramFile

# After:
from schema.yaml_schema import ClassDiagramFile
```

**Step 4: Verify no remaining mdf_server imports**

```bash
grep -rn "mdf_server" /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/tools/
```

Expected: no output.

---

### Task 4: Create engine and cli stubs

**Files:**
- Create: `SIM/engine/__init__.py`
- Create: `SIM/cli/test_harness.py`
- Create: `SIM/cli/gui.py`

**Step 1: Write engine stub**

`SIM/engine/__init__.py`:
```python
"""
engine — MDF simulation engine.
Stub: implemented in Phase 5 (05-simulation).
"""
```

**Step 2: Write cli test harness stub**

`SIM/cli/test_harness.py`:
```python
"""
cli.test_harness — CLI test harness entry point (mdf-sim-test).
Stub: implemented in Phase 5 (05-simulation).
"""


def main() -> None:
    """Entry point for mdf-sim-test CLI command."""
    print("mdf-sim-test: not yet implemented")
```

**Step 3: Write cli gui stub**

`SIM/cli/gui.py`:
```python
"""
cli.gui — Dear PyGui interface entry point (mdf-sim-gui).
Stub: implemented in Phase 5 (05-simulation).
"""


def main() -> None:
    """Entry point for mdf-sim-gui CLI command."""
    print("mdf-sim-gui: not yet implemented")
```

---

### Task 5: Copy and update tests

**Files:**
- Copy + modify: `REPO/mdf-server/tests/test_yaml_schema.py` → `SIM/tests/test_yaml_schema.py`
- Copy + modify: `REPO/mdf-server/tests/test_drawio_schema.py` → `SIM/tests/test_drawio_schema.py`
- Copy + modify: `REPO/mdf-server/tests/test_model_io.py` → `SIM/tests/test_model_io.py`
- Copy + modify: `REPO/mdf-server/tests/test_roundtrip.py` → `SIM/tests/test_roundtrip.py`

**Step 1: Copy test files**

```bash
cp /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-server/tests/test_yaml_schema.py \
   /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/tests/test_yaml_schema.py

cp /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-server/tests/test_drawio_schema.py \
   /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/tests/test_drawio_schema.py

cp /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-server/tests/test_model_io.py \
   /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/tests/test_model_io.py

cp /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-server/tests/test_roundtrip.py \
   /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/tests/test_roundtrip.py
```

**Step 2: Check all mdf_server references that need updating**

```bash
grep -n "mdf_server" /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/tests/*.py
```

Expected: every line will reference `mdf_server.schema.*` or `mdf_server.tools.*`.

**Step 3: Update test_yaml_schema.py**

Replace all occurrences of `from mdf_server.schema.yaml_schema import` with `from schema.yaml_schema import`.

```bash
sed -i 's/from mdf_server\.schema\.yaml_schema import/from schema.yaml_schema import/g' \
    /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/tests/test_yaml_schema.py
```

**Step 4: Update test_drawio_schema.py**

```bash
sed -i 's/from mdf_server\.schema\.drawio_schema import/from schema.drawio_schema import/g' \
    /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/tests/test_drawio_schema.py
```

**Step 5: Update test_roundtrip.py**

```bash
sed -i 's/from mdf_server\.schema\.drawio_schema import/from schema.drawio_schema import/g' \
    /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/tests/test_roundtrip.py
```

**Step 6: Update test_model_io.py**

This file has several patterns:
- `import mdf_server.server` → remove (server is not in mdf-sim)
- `import mdf_server.tools.model_io` → `import tools.model_io`
- `import mdf_server.tools.drawio` → `import tools.drawio`
- `import mdf_server.tools.validation` → `import tools.validation`
- `import mdf_server.tools.simulation` → `import tools.simulation`
- `import mdf_server.pycca` → `import pycca`
- `from mdf_server.tools import model_io` → `from tools import model_io`

Apply all replacements:

```bash
sed -i \
  -e 's/import mdf_server\.server.*$/import tools.model_io  # smoke test/' \
  -e 's/import mdf_server\.tools\.model_io/import tools.model_io/' \
  -e 's/import mdf_server\.tools\.drawio/import tools.drawio/' \
  -e 's/import mdf_server\.tools\.validation/import tools.validation/' \
  -e 's/import mdf_server\.tools\.simulation/import tools.simulation/' \
  -e 's/import mdf_server\.pycca/import pycca/' \
  -e 's/from mdf_server\.tools import model_io/from tools import model_io/' \
  /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/tests/test_model_io.py
```

**Step 7: Verify no remaining mdf_server references**

```bash
grep -n "mdf_server" /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/tests/*.py
```

Expected: no output.

**Step 8: Create tests/__init__.py**

```bash
touch /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/tests/__init__.py
```

---

### Task 6: Copy docs and planning files

**Step 1: Copy simulation engine design doc**

```bash
cp /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-sim/docs/2026-03-06-simulation-engine-design.md \
   /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/docs/2026-03-06-simulation-engine-design.md
```

**Step 2: Copy phase planning directories (phases 01, 02, 03)**

```bash
cp -r /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/.planning/phases/01-schema-foundation \
      /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/.planning/phases/01-schema-foundation

cp -r /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/.planning/phases/02-mcp-server-model-io \
      /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/.planning/phases/02-mcp-server-model-io

cp -r /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/.planning/phases/03-validation-tool \
      /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/.planning/phases/03-validation-tool
```

**Step 3: Copy research directory**

```bash
cp -r /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/.planning/research \
      /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/.planning/research
```

**Step 4: Copy GUIDELINES.md**

```bash
cp /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/.planning/GUIDELINES.md \
   /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator/.planning/GUIDELINES.md
```

---

### Task 7: Write mdf-simulator planning docs (PROJECT, REQUIREMENTS, ROADMAP, STATE)

**Files:**
- Create: `SIM/.planning/PROJECT.md`
- Create: `SIM/.planning/REQUIREMENTS.md`
- Create: `SIM/.planning/ROADMAP.md`
- Create: `SIM/.planning/STATE.md`

**Step 1: Create PROJECT.md**

`SIM/.planning/PROJECT.md` — scope to tools/schema. Copy from backup at `BACKUP/.planning/PROJECT.md` and trim to remove agent/skill/workflow sections, keeping only the schema, tools, and simulation content. Update the heading to clarify this is the simulator library scope.

Key edits to make after copying:
- Title: `# MDF Simulator (mdf-sim)`
- Remove Milestone 1 (skills) and Milestone 2 (code-gen workflow) active requirements — those are mdf-server scope
- Keep: schema, MCP tools (model CRUD, Draw.io, validation, simulation), pycca, code generation targets

**Step 2: Create REQUIREMENTS.md**

Copy `BACKUP/.planning/REQUIREMENTS.md` to `SIM/.planning/REQUIREMENTS.md`, then delete all requirement blocks that are NOT in the MCP-00 through MCP-09 range (i.e., remove AGENT-*, SKILL-*, REF-* sections).

**Step 3: Create ROADMAP.md**

Copy `BACKUP/.planning/ROADMAP.md` to `SIM/.planning/ROADMAP.md`, then:
- Delete Phase 7 through Phase 10 sections entirely
- Update the Progress table to only show Phases 1–6
- Update the header/overview to reflect simulator library scope

**Step 4: Create STATE.md**

Copy `BACKUP/.planning/STATE.md` to `SIM/.planning/STATE.md`. Update:
- Line 1: `milestone_name: mdf-simulator v0.1`
- `stopped_at: Migration from monorepo — ready to continue Phase 3`
- `last_activity: 2026-03-09 — Migrated from model-based-project-framework monorepo`
- Remove mdf-server specific entries from `### Decisions` that are about FastMCP registration, submodule, etc.

---

### Task 8: Create mdf-simulator pyproject.toml + uv setup

**Files:**
- Create: `SIM/pyproject.toml`

**Step 1: Write pyproject.toml**

`SIM/pyproject.toml`:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mdf-sim"
version = "0.1.0"
description = "MDF simulation engine, schema, and tools"
requires-python = ">=3.11"
dependencies = [
    "defusedxml>=0.7.1",
    "lxml>=6.0.2",
    "pydantic>=2.12.5",
    "pyyaml>=6.0.3",
    "ruamel-yaml>=0.19.1",
]

[project.scripts]
mdf-sim-test = "cli.test_harness:main"
mdf-sim-gui = "cli.gui:main"

[tool.hatch.build.targets.wheel]
packages = ["schema", "pycca", "tools", "engine", "cli"]

[dependency-groups]
dev = [
    "mypy>=1.19.1",
    "pytest>=9.0.2",
    "ruff>=0.15.5",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

**Step 2: Create uv environment and install**

```bash
cd /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator
uv sync --dev
```

Expected: uv creates `.venv/`, installs pydantic, pyyaml, etc., writes `uv.lock`.

**Step 3: Verify package is importable**

```bash
cd /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator
uv run python -c "from schema.yaml_schema import ClassDiagramFile; print('OK')"
```

Expected: `OK`

---

### Task 9: Run tests in mdf-simulator

**Step 1: Run the full test suite**

```bash
cd /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator
uv run pytest tests/ -v
```

Expected: all tests pass. If any fail, consult `BACKUP/mdf-server/tests/` to compare and fix import paths.

Common failure patterns to look for:
- `ModuleNotFoundError: No module named 'mdf_server'` — missed an import replacement in step 5
- `ModuleNotFoundError: No module named 'schema'` — package not installed, re-run `uv sync`

**Step 2: Confirm test count matches original**

```bash
cd /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-server
uv run pytest tests/ -v --ignore=tests/test_templates.py --co -q 2>&1 | tail -5
```

Compare test count to mdf-simulator run — should be equal (minus test_templates.py).

---

### Task 10: Initialize mdf-simulator git repo and push

**Step 1: Create .gitignore**

`SIM/.gitignore`:
```
.venv/
__pycache__/
*.pyc
.pytest_cache/
*.egg-info/
dist/
```

**Step 2: Initialize git and make initial commit**

```bash
cd /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator
git init
git add .
git commit -m "feat: initial commit — migrated from model-based-project-framework monorepo"
```

**Step 3: Add remote and push**

At this point, provide the remote URL for mdf-simulator and run:

```bash
cd /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator
git remote add origin <REMOTE_URL>
git push -u origin master
```

Pause here and ask user for the remote URL before proceeding.

---

### Task 11: Replace mdf-sim/docs with git submodule in mdf-server

**Step 1: Remove the existing mdf-sim/ docs directory**

```bash
cd /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework
rm -rf mdf-sim/
```

**Step 2: Add mdf-simulator as a submodule at mdf-sim/**

```bash
cd /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework
git submodule add <REMOTE_URL> mdf-sim
```

Expected: `mdf-sim/` directory appears, `.gitmodules` file created.

**Step 3: Verify submodule contents**

```bash
ls /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-sim/
```

Expected: `schema/`, `tools/`, `pycca/`, `engine/`, `cli/`, `tests/`, `docs/`, `pyproject.toml`, etc.

---

### Task 12: Update mdf-server pyproject.toml

**Files:**
- Modify: `REPO/mdf-server/pyproject.toml`

**Step 1: Write updated pyproject.toml**

Replace the entire file contents:

```toml
[project]
name = "mdf-server"
version = "0.1.0"
description = "MDF MCP server — Claude interface for mdf-sim"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "fastmcp>=3.1.0,<4.0.0",
    "mdf-sim",
]

[project.scripts]
mdf-server = "mdf_server.server:main"

[tool.uv.sources]
mdf-sim = { path = "../mdf-sim", editable = true }

[dependency-groups]
dev = [
    "mypy>=1.19.1",
    "pytest>=9.0.2",
    "ruff>=0.15.5",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

Note: path is `../mdf-sim` because pyproject.toml is inside `mdf-server/` subdirectory, so `../mdf-sim` resolves to `model-based-project-framework/mdf-sim/`.

**Step 2: Sync dependencies**

```bash
cd /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-server
uv sync --dev
```

Expected: uv installs fastmcp and mdf-sim (editable from submodule), regenerates uv.lock.

**Step 3: Verify mdf-sim is importable from mdf-server venv**

```bash
cd /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-server
uv run python -c "from tools.model_io import list_domains; print('OK')"
```

Expected: `OK`

---

### Task 13: Update mdf-server/server.py imports

**Files:**
- Modify: `REPO/mdf-server/mdf_server/server.py`

**Step 1: Update the import line**

Current `server.py`:
```python
from mdf_server.tools.model_io import list_domains, read_model, write_model
```

Updated `server.py`:
```python
"""MDF MCP server — FastMCP entry point."""
from fastmcp import FastMCP
from tools.model_io import list_domains, read_model, write_model

mcp = FastMCP("mdf")

mcp.tool(list_domains)
mcp.tool(read_model)
mcp.tool(write_model)


def main() -> None:
    """Start the MDF MCP server with stdio transport."""
    mcp.run()


if __name__ == "__main__":
    main()
```

**Step 2: Verify server is importable**

```bash
cd /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-server
uv run python -c "import mdf_server.server; print('OK')"
```

Expected: `OK`

---

### Task 14: Remove migrated source files from mdf-server

**Step 1: Delete schema, pycca, tools subdirectories from mdf_server package**

```bash
rm -rf /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-server/mdf_server/schema/
rm -rf /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-server/mdf_server/pycca/
rm -rf /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-server/mdf_server/tools/
```

**Step 2: Delete migrated tests from mdf-server**

```bash
rm /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-server/tests/test_yaml_schema.py
rm /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-server/tests/test_drawio_schema.py
rm /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-server/tests/test_model_io.py
rm /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-server/tests/test_roundtrip.py
```

**Step 3: Verify mdf_server package still imports**

```bash
cd /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-server
uv run python -c "import mdf_server.server; print('OK')"
```

Expected: `OK`

**Step 4: Run remaining mdf-server tests**

```bash
cd /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-server
uv run pytest tests/ -v
```

Expected: `test_templates.py` tests pass.

---

### Task 15: Update mdf-server planning docs

**Files:**
- Modify: `REPO/.planning/PROJECT.md`
- Modify: `REPO/.planning/REQUIREMENTS.md`
- Modify: `REPO/.planning/ROADMAP.md`
- Modify: `REPO/.planning/STATE.md`

**Step 1: Update PROJECT.md**

Edit `REPO/.planning/PROJECT.md`:
- Update title/scope: `# MDF Server (mdf-server) — Claude Interface`
- Remove all MCP tool requirements (those belong to mdf-simulator)
- Keep: FastMCP server, Phase 0 skills, agents, workflow requirements
- Add note: "Schema, tools, and simulation engine live in `mdf-sim/` (submodule → mdf-simulator)"

**Step 2: Update REQUIREMENTS.md**

Edit `REPO/.planning/REQUIREMENTS.md`:
- Remove MCP-00 through MCP-09 requirement blocks
- Keep AGENT-*, SKILL-*, REF-* blocks
- Add preamble note: "MCP tool requirements (MCP-00..MCP-09) are tracked in mdf-simulator"

**Step 3: Update ROADMAP.md**

Edit `REPO/.planning/ROADMAP.md`:
- Remove Phases 1–6 detail sections
- Keep Phases 7–10 detail sections
- Replace Phase 1–6 entries in the Phases list with a single summary line:
  `- [x] **Phases 1–6: Schema + Tools** — Implemented in mdf-simulator repository`
- Update Progress table to only track Phases 7–10

**Step 4: Update STATE.md**

Edit `REPO/.planning/STATE.md`:
- Update `stopped_at: Repo split complete — ready to plan Phase 7`
- Update `last_activity: 2026-03-09 — Split monorepo into mdf-simulator + mdf-server`
- Update `completed_phases: 0` (phases 1–6 are in mdf-simulator now)
- Remove Phase 1–6 phase state rows from the table
- Remove Phase 1–2 decisions that are tool/schema specific (those are in mdf-simulator STATE.md)

---

### Task 16: Commit mdf-server and verify final state

**Step 1: Check what changed**

```bash
cd /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework
git status
git diff --stat
```

Review: deleted files from mdf_server/, updated pyproject.toml, updated server.py, updated .planning/, new .gitmodules, new mdf-sim/ submodule entry.

**Step 2: Run full mdf-server test suite one final time**

```bash
cd /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/mdf-server
uv run pytest tests/ -v
```

Expected: all pass.

**Step 3: Run mdf-simulator tests one final time**

```bash
cd /c/Users/bchaloux/Local_Documents/Local_Repos/mdf-simulator
uv run pytest tests/ -v
```

Expected: all pass.

**Step 4: Commit mdf-server changes**

```bash
cd /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework
git add -A
git commit -m "refactor: split monorepo — mdf-simulator submodule at mdf-sim/, server is now thin adapter"
```

**Step 5: Confirm .gitmodules is correct**

```bash
cat /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework/.gitmodules
```

Expected:
```
[submodule "mdf-sim"]
    path = mdf-sim
    url = <REMOTE_URL>
```

---

### Task 17: Delete backup

Once everything is verified working:

```bash
rm -rf /c/Users/bchaloux/Local_Documents/Local_Repos/model-based-project-framework-backup
```

Confirm with user before running this step.
