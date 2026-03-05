# Model-Driven Framework (MDF)

## What This Is

A design-first development workflow for embedded and real-world systems using the Shlaer-Mellor xUML methodology. Engineers build a fully verified behavioral model before any code is written, then feed that model into a modified GSD execution pipeline. The framework is divided into four phases: Design (Phase 0), Model Verification (Phase 1), Target Configuration (Phase 2), and Implementation (Phase 3+).

**Architecture:** MDF owns the design and planning layers (Phase 0–2) through custom agents and an MCP server workbench. GSD owns the execution and tracking layers (Phase 3+). The artifact schemas (PLAN.md, CONTEXT.md, STATE.md) are the contract between them — our agents produce them, GSD's executor consumes them.

## Current Milestone: v1.0 — Foundation

**Goal:** Deliver the schema definitions, MCP server workbench, and Phase 0 skills that enable an engineer to build a verified domain model from scratch.

**Target features:**
- Schema Foundation: YAML model schema, canonical Draw.io schema, behavior doc format, folder structure templates
- MCP Server (Python/FastMCP): 8 tools for model CRUD, Draw.io rendering, validation (graph reachability), and simulation
- Phase 0 Skills: `/mdf:new-project`, `/mdf:discuss-domain`, `/mdf:discuss-class`, `/mdf:discuss-state`, `/mdf:review-model`, `/mdf:verify-model`, `/mdf:configure-target`, `/mdf:pause`, `/mdf:resume`, `/mdf:plan-roadmap`

## Core Value

Engineers can verify the full structural design before typing `execute-phase` — no guessing, no mid-execution surprises.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] MCP server with tools for YAML model CRUD, Draw.io rendering, structural validation, and Draw.io sync
- [ ] YAML semantic model format aligned with xUML/Shlaer-Mellor methodology — classes, associations, state machines, pycca action language, domain bridges
- [ ] Draw.io XML generation from YAML model (human-facing view only — canonical 1:1 schema)
- [ ] Structural validation with graph reachability checks — produces actionable per-issue error list (not pass/fail)
- [ ] State machine simulation — interprets pycca action language from YAML, runs event sequences, returns execution trace
- [ ] **Milestone 1** — Model creation (entirely custom, no GSD equivalent):
  - [ ] `/design:start` skill — engineering domain questioning (classes, associations, state machines, domain bridges)
  - [ ] Custom domain modeling agents — iterative model building through conversation
  - [ ] Custom model validation agents — graph reachability, structural checks, model review/approval flow
  - [ ] Soft guidelines document artifact — templated sections with escape hatch
- [ ] **Milestone 2** — Model-to-code (custom planning agents + GSD execution layer):
  - [ ] Custom discuss-phase agent — model-aware context gathering, presents pre-answered decisions, surfaces model gaps only
  - [ ] Custom researcher agent — "how to implement the model" brief, not "how to structure the code"
  - [ ] Custom planner agent — reads YAML model as authoritative, references model specs in every task, model conformance in must_haves
  - [ ] Guidelines checker agent — runs per executor chunk, reviews code against guidelines
  - [ ] GSD executor, verifier, and tracking reused unchanged — consume our PLAN.md/CONTEXT.md output
- [ ] C code generation path — YAML → pycca DSL → pycca compiler → C
- [ ] Python code generation target (simulation/test path)

### Out of Scope

- Modifying GSD files — GSD is updated periodically; all customizations live in skills and this MCP package
- Micca as compilation target — pycca is the chosen path; Micca deferred
- State machine simulation is v1 — required for behavioral verification before code
- Multi-user collaboration — single engineer context for now

## Context

Built from direct experience with GSD on a previous project: GSD's questioning and planning phases ask good product questions ("what do you want to build?") but skip engineering questions ("what are your domains, what classes exist, what are the state machines, what are the subsystem interfaces?"). The result is that `execute-phase` produces structurally unexpected code — Claude makes implementation decisions that the engineer would have made differently if asked upfront.

The framework adopts **Shlaer-Mellor Executable UML** methodology, already in use at Dilon Technologies. Key references:
- *Models to Code* (Starr, Mangogna, Mellor — Apress 2017)
- Leon Starr's modelint GitHub: https://github.com/modelint
- Micca / pycca model compilers: http://repos.modelrealization.com

The YAML semantic model is Claude's native working format — one file per domain subsystem. Claude never needs to load the whole model at once, keeping context footprint small.

## Constraints

- **Package**: Standalone — this repo (`model-based-project-framework`), not added to `dilon-claude-tools`
- **GSD compatibility**: Build on top of GSD, never modify GSD files
- **Code gen targets**: C (embedded) and Python (simulation) for v1
- **Skill namespace**: `/mdf:` — Model-Driven Framework commands
- **MCP server**: Python (FastMCP 3.1.0) — better library support for pycca parsing and graph traversal; standalone package at `mdf-server/`
- **Model files**: `.design/model/` — top-level `.design/` directory parallel to `.planning/`
- **Guidelines checker**: Runs at executor level (per planner task chunk), same pass as other code quality agents — configured in `config.json`
- **Skills location**: `.claude/skills/mdf/` — scoped to project repo, never inside GSD directories

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| MCP workbench over skills-only | Skills alone can't read/update .drawio after writing — design iteration is blind without MCP state | — Pending |
| YAML as source of truth (not Draw.io) | Claude generates and reasons about YAML reliably; Draw.io is a presentation view only | — Pending |
| Canonical Draw.io schema (1:1 with YAML) | Bijection means sync_from_drawio is a structured parse, not interpretation — round-trip is deterministic | — Pending |
| pycca action language in YAML | User knows C; pycca is well-documented, targets embedded C, enables simulation and code generation | — Pending |
| `.design/` as top-level directory | Separates design artifacts from planning artifacts; room to grow beyond models | — Pending |
| Python/FastMCP for MCP server | Better library support for pycca parsing and graph traversal than TypeScript | — Pending |
| Guidelines checker at executor level | Planner task chunks are already context-sized; checking per chunk gives full coverage without a separate phase-level sweep | — Pending |
| Simulation is v1 (not like-to-have) | pycca action language in YAML makes behavioral verification before code possible — this is the core value | — Pending |
| Artifact set: YAML + guidelines only | Draw.io is human-facing view; interface contracts are expressed in YAML as domain bridges | — Pending |
| Single `/design:start` skill to start | Ship one comprehensive skill first; decompose if it gets unwieldy | — Pending |
| Soft guidelines: template with escape hatch | Standard sections as defaults; any section skippable or addable | — Pending |
| Custom agents own the planning layer | Injecting model knowledge into GSD agents fights their defaults; custom agents have it natively | — Pending |
| GSD owns execution and tracking only | gsd-executor, gsd-verifier, STATE.md, ROADMAP.md reused unchanged — artifact schemas are the contract | — Pending |
| Two distinct milestones | Milestone 1 (model creation) is entirely novel; Milestone 2 (model-to-code) produces GSD-compatible artifacts | — Pending |

---
*Last updated: 2026-03-05 after full workflow design — MDF framework renamed, Phase 0–2 custom workflow defined, GSD integration boundaries locked*
