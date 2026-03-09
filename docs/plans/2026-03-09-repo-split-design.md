# Repo Split Design: mdf-simulator + mdf-server

*Date: 2026-03-09*

## Summary

Split the `model-based-project-framework` monorepo into two focused repositories:

- **`mdf-simulator`** — standalone Python library owning the schema, tools, and simulation engine
- **`mdf-server`** (current repo) — thin FastMCP adapter that exposes mdf-simulator's tools to Claude via MCP

The simulator is a git submodule inside mdf-server, mounted at `mdf-sim/` and installed as an editable path dependency.

---

## Repositories

### mdf-simulator

**Purpose:** Standalone Python library. Schema definitions, all tool implementations, pycca parser, simulation engine, and CLI entry points. Independently usable without Claude or MCP.

**Remote:** Exists — to be connected after `git init`.

**Layout (flat — repo root is package source):**

```
mdf-simulator/
├── schema/
│   ├── __init__.py
│   ├── yaml_schema.py
│   └── drawio_schema.py
├── pycca/
│   └── __init__.py
├── tools/
│   ├── __init__.py
│   ├── model_io.py
│   ├── validation.py
│   ├── drawio.py
│   └── simulation.py
├── engine/
│   └── __init__.py          (stub — Phase 5)
├── cli/
│   ├── __init__.py
│   ├── test_harness.py      (stub — mdf-sim-test entry point)
│   └── gui.py               (stub — mdf-sim-gui entry point)
├── tests/
│   ├── test_yaml_schema.py
│   ├── test_drawio_schema.py
│   ├── test_model_io.py
│   └── test_roundtrip.py
├── docs/
│   └── 2026-03-06-simulation-engine-design.md
├── .planning/
│   ├── phases/
│   │   ├── 01-schema-foundation/
│   │   ├── 02-mcp-server-model-io/
│   │   └── 03-validation-tool/
│   ├── research/
│   ├── PROJECT.md
│   ├── REQUIREMENTS.md      (MCP-00 through MCP-09)
│   ├── ROADMAP.md           (Phases 1–6)
│   ├── STATE.md
│   └── GUIDELINES.md
└── pyproject.toml
```

**Package configuration:** Project name `mdf-sim`, package root mapped to repo root so imports resolve as `from mdf_sim.schema import ...`, `from mdf_sim.tools import ...`. CLI entry points `mdf-sim-test` and `mdf-sim-gui` declared but stubbed.

**Dependencies:** pydantic, pyyaml, ruamel-yaml, lxml, defusedxml (all migrated from mdf-server).

**Git:** Fresh `git init` — no history carried over. Connect to existing remote after init.

---

### mdf-server (current repo)

**Purpose:** FastMCP adapter. Registers mdf-simulator's tool implementations as MCP endpoints for Claude. No business logic lives here.

**Layout:**

```
model-based-project-framework/
├── mdf_server/
│   ├── __init__.py
│   └── server.py            (imports tools from mdf_sim, registers via FastMCP)
├── mdf-sim/                 (git submodule → mdf-simulator repo)
├── templates/               (model artifact templates — unchanged)
├── docs/                    (workflow and design docs)
├── tests/
│   └── test_templates.py
├── .planning/
│   ├── phases/              (empty — phases 07+ not yet planned)
│   ├── PROJECT.md           (scoped to Claude interface and workflow)
│   ├── REQUIREMENTS.md      (AGENT-*, SKILL-*, REF-* requirements only)
│   ├── ROADMAP.md           (Phases 7–10 only)
│   ├── STATE.md             (reset to new baseline)
│   ├── GUIDELINES.md
│   └── config.json
└── pyproject.toml           (dep: mdf-sim = {path = "./mdf-sim"}, drops migrated deps)
```

**Dependencies:** fastmcp, mdf-sim (via submodule path). All schema/parsing deps removed (now owned by mdf-sim).

**Git:** Current repo — history preserved for files that stay. Files moved to mdf-simulator are deleted from this repo after the split.

---

## Submodule Setup

```
# Inside mdf-server repo after mdf-simulator remote is ready:
git submodule add <mdf-simulator-remote-url> mdf-sim
```

The existing `mdf-sim/` directory (docs only) is deleted before the submodule is added.

---

## Planning Doc Split

| Document | mdf-simulator | mdf-server |
|----------|--------------|------------|
| PROJECT.md | Tools/schema scope | Workflow/Claude interface scope |
| REQUIREMENTS.md | MCP-00 through MCP-09 | AGENT-*, SKILL-*, REF-* |
| ROADMAP.md | Phases 1–6 | Phases 7–10 |
| STATE.md | Sim-relevant state | Reset — new baseline |
| GUIDELINES.md | Copied to both | Copied to both |
| phases/ | 01, 02, 03 directories | Empty (07+ not planned yet) |
| research/ | Full research dir | Not copied |
| config.json | Not copied | Stays |

---

## File Migration Summary

### Moves to mdf-simulator
- `mdf-server/mdf_server/schema/` → `schema/`
- `mdf-server/mdf_server/pycca/` → `pycca/`
- `mdf-server/mdf_server/tools/` → `tools/`
- `mdf-server/tests/` (all except test_templates.py) → `tests/`
- `mdf-sim/docs/` → `docs/`
- `.planning/phases/01-schema-foundation/` → `.planning/phases/01-schema-foundation/`
- `.planning/phases/02-mcp-server-model-io/` → `.planning/phases/02-mcp-server-model-io/`
- `.planning/phases/03-validation-tool/` → `.planning/phases/03-validation-tool/`
- `.planning/research/` → `.planning/research/`
- `.planning/GUIDELINES.md` → `.planning/GUIDELINES.md`

### Stays in mdf-server
- `mdf_server/server.py` (updated imports)
- `templates/`
- `docs/`
- `tests/test_templates.py`
- `.planning/config.json`
- `.planning/GUIDELINES.md` (copy)

### New in mdf-simulator
- `engine/__init__.py` (stub)
- `cli/__init__.py`, `cli/test_harness.py`, `cli/gui.py` (stubs)
- `pyproject.toml` (new)

### Updated in mdf-server
- `pyproject.toml` — new dep on `./mdf-sim`, migrated deps removed
- `mdf_server/server.py` — imports updated to `from mdf_sim.tools import ...`
- `.planning/PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, `STATE.md` — scoped to workflow
