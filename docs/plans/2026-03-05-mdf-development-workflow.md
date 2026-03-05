# MDF Development Workflow — Design Doc

**Date:** 2026-03-05
**Status:** Design complete — ready for implementation planning
**Skill namespace:** `/mdf`

---

## Overview

The Model-Driven Framework (MDF) is a design-first development workflow for embedded and real-world systems using the Shlaer-Mellor xUML methodology. It produces a fully verified behavioral model before any code is written, then feeds that model into a modified GSD execution pipeline.

The framework is divided into four phases: Design (Phase 0), Model Verification (Phase 1), Target Configuration (Phase 2), and Implementation (Phase 3+). GSD's planning and execution infrastructure is only introduced in Phase 3.

---

## Directory Structure

```
.planning/
  PROJECT.md
  MILESTONES.md
  ROADMAP.md
  STATE.md
  GUIDELINES.md           # Engineering conventions; refined during early Phase 3

.design/
  model/
    DOMAINS.md            # Domain map with realized domains and bridges
    <domain>/
      class-diagram       # Class diagram for the domain
      state-diagrams/     # One or more state diagrams per domain
  behavior/
    <domain>/
      domain.md           # Domain-level behavioral spec
      <class>.md          # Class-level behavioral spec
      <state-machine>.md  # State machine behavioral spec
  research/
    FEATURES.md
    PITFALLS.md
    STACK.md              # Updated during Phase 2; refined during Phase 3
    SUMMARY.md
    TRANSLATION.md        # Model-to-code mapping for the target; refined during Phase 3
```

---

## Phase 0: Design

The design phase is entirely custom — no GSD agents. It is multi-session and produces the full structural and behavioral model of the system.

### Stage 1 — Domain Questioning

**Input:** Problem statement + engineer intent

**Agents:**
- Questioner — extracts domain structure through conversation
- Domain-verifier — runs at the end of each step, checks model consistency

**Output:**
- `.design/model/DOMAINS.md` — domain map with realized domains and bridges
- `.design/behavior/<domain>/domain.md` — initial behavioral specs per domain
- `.planning/research/` — FEATURES, PITFALLS, STACK, SUMMARY

The researcher is divided into two agents:
- **Researcher** — focuses on features, pitfalls, and stack
- **Architect** — focuses solely on architecture; produces the domain map identifying domain boundaries, realized domains, and bridge interfaces

DOMAINS.md is a living document — it is not frozen after this stage. It evolves throughout the project.

### Stage 2 — Class Diagram Planning

**Input:** DOMAINS.md, behavior/ docs

**Agents:**
- Class diagram agent — extracts class structure through questioning
- Domain-verifier — runs at end of each step

**Output:**
- Class diagram per domain (`.design/model/<domain>/class-diagram`)
- `.design/behavior/<domain>/<class>.md` — class-level behavioral specs (extended)

**Sequencing:** Developer may choose to fully complete one domain (class diagrams + state diagrams) before moving to the next, or do all class diagrams first. This depends on how well domain boundaries are established. If there is uncertainty, proceed class-by-class.

**Bridge refinement:** Once both class diagrams that a bridge references are complete, the domain-verifier runs a consistency check on that bridge.

### Stage 3 — State Diagram Planning

**Input:** Class diagrams, behavior/ docs

**Agents:**
- State diagram agent — extracts state machine structure through questioning
- Domain-verifier — runs at end of each step

**Output:**
- State diagrams per domain (`.design/model/<domain>/state-diagrams/`)
- `.design/behavior/<domain>/<state-machine>.md` — state machine behavioral specs (extended)

### Domain-Verifier Rules

- Runs at the end of each planning step across all three stages
- Reports to the calling agent: pass or list of specific inconsistencies
- Does not produce a persistent artifact
- Checks that class-level and state machine behaviors are consistent with (not contradictory to) the domain-level behavior they fall under
- More granular scope (class, state machine) takes precedence over broader scope (domain) when conflicts arise
- Checks bridge consistency once both referenced class diagrams are complete

---

## Phase 1: Model Verification

**Input:** Full model (`.design/model/`) + behavior docs (`.design/behavior/`)

**Agents:**
- Simulation test generator — reads behavior docs, produces test suite from realized bridge inputs
- Domain-verifier — final full-model consistency check

**Output:**
- Simulation test suite
- Simulation results (pass/fail per behavioral spec)

**Visual review:** Engineer reviews each diagram in Draw.io before simulation runs.

**Test coverage:** Behavior docs drive test generation. Inputs come through realized bridges. Coverage is measured against the behavioral specs.

---

## Phase 2: Target Configuration

**Input:** Verified model, STACK.md, board specs (if provided in Stage 1 research)

**Agents:**
- Execution domain agent — generates execution domain implementation from metamodel rules + target specs; minimal user input required for target-specific architectural decisions

**Output:**
- Updated `STACK.md`
- `TRANSLATION.md` — how to implement the metamodel execution domain contract on this target
- Execution domain implementation (the runtime substrate all domain models run on)
- Target repo(s) — one per target; either git submodules or subdirectories of a parent directory
- Dev environment(s) per target

**Note:** The execution domain is part of the metamodel, not the model. It is the fixed contract that all action language translation must conform to. TRANSLATION.md is the project+target-specific guide for implementing that contract.

**Multi-session:** Target configuration may span multiple sessions, especially with multiple targets.

After Phase 2, model verification should be largely automated. Re-running verification after model updates requires minimal time.

---

## Phase 3+: Implementation (per target repo)

Each target repo gets its own GSD project. All GSD phases reference back to `.design/` in the shared model repo (via submodule or parent directory path).

### Custom: Researcher → CONTEXT.md

The standard GSD discuss-phase is replaced by a custom researcher that:
- Reads the verified model (`.design/model/`)
- Reads TRANSLATION.md and GUIDELINES.md
- Produces a model-aware CONTEXT.md — structural decisions are pre-answered from the model

No significant user discussion is needed for CONTEXT.md generation. The researcher operates largely autonomously.

**GUIDELINES.md refinement:** Event-driven. When the engineer comments on code format or patterns during Phase 3 execution, the researcher flags it and updates GUIDELINES.md.

**TRANSLATION.md refinement:** Same pattern — refined during early Phase 3 runs as the engineer's preferences for model-to-code mapping emerge from seeing actual code. After 3–4 implementation runs, both documents should be stable.

### Stock GSD (unchanged)

- GSD planner — reads CONTEXT.md, produces PLAN.md
- GSD plan-verifier — verifies plan conforms to model (via CLAUDE.md injection)
- GSD executor — implements per plan, reads model per CLAUDE.md instruction

### Model-Updater Agent

A reactive agent (not a scheduled step) that can be invoked when:
- Bugs or issues found during testing reveal model inconsistencies
- Project scope changes require model revision

The model-updater can modify any `.design/` or `.planning/` document. After a model update, the simulation test suite is re-run automatically. The model test generator agent adds new tests as needed to cover the updated model.

---

## Entry Point

`/mdf:new-project` — bootstraps `.planning/` and `.design/`, initializes DOMAINS.md, and kicks off Stage 1 domain questioning.

---

## Deliverable List

### MCP Server (Python/FastMCP)
- `read_model(domain)`
- `write_model(domain, yaml)`
- `list_domains()`
- `render_to_drawio(domain)`
- `validate_drawio(domain, xml)`
- `sync_from_drawio(domain, xml)`
- `validate_model(domain)`
- `simulate_state_machine(class, events)`

### Schemas / Templates
- YAML model schema (classes, associations, state machines, bridges, pycca action language)
- Canonical Draw.io schema (1:1 with YAML)
- Behavior doc format (domain / class / state machine)
- DOMAINS.md template
- CLASS_DIAGRAM.md template
- STATE_DIAGRAM.md template
- TRANSLATION.md template
- Folder structure (`.planning/`, `.design/model/`, `.design/behavior/`, `.design/research/`)

### Agents
- Domain Architect — domain map, boundaries, bridges → DOMAINS.md
- Project Researcher — features, pitfalls, stack → research/ docs
- Class Diagram Agent — class structure through questioning → class diagrams + behavior docs
- State Diagram Agent — state machine structure through questioning → state diagrams + behavior docs
- Domain Verifier — consistency checker, runs at end of each planning step
- Simulation Test Generator — behavior docs → test suite
- Execution Domain Agent — generates execution domain from metamodel rules + target specs
- Phase Researcher — reads model + TRANSLATION.md → CONTEXT.md; refines GUIDELINES + TRANSLATION
- Model Updater — reactive agent for model corrections and scope changes
- Guidelines Checker — runs per executor chunk against GUIDELINES

### Skills (Phase 0–2)
- `/mdf:new-project`
- `/mdf:discuss-domain`
- `/mdf:discuss-class`
- `/mdf:discuss-state`
- `/mdf:review-model`
- `/mdf:verify-model`
- `/mdf:configure-target`
- `/mdf:pause`
- `/mdf:resume`
- `/mdf:plan-roadmap`

### Skills (Phase 3+)
- `/mdf:discuss-phase`
- `/mdf:plan-phase`
- `/mdf:execute-phase`
- `/mdf:verify-work`
- `/mdf:complete-milestone`
- `/mdf:new-milestone`
- `/mdf:update-model`

---

## GSD Integration

### Using Verbatim

**Agents:**
- `gsd-executor` — executes phase plans unchanged; receives richer context via CLAUDE.md injection
- `gsd-planner` — produces PLAN.md unchanged; receives model-aware CONTEXT.md as input
- `gsd-plan-checker` — verifies plans unchanged; picks up model references via CLAUDE.md
- `gsd-verifier` — verifies work unchanged; picks up model references via CLAUDE.md

**Artifact formats:**
- PLAN.md
- STATE.md
- ROADMAP.md
- MILESTONES.md
- PROJECT.md
- REQUIREMENTS.md

**Skills (available in Phase 3+ alongside MDF wrappers):**
- `/gsd:progress`
- `/gsd:pause-work` / `/gsd:resume-work`
- `/gsd:check-todos` / `/gsd:add-todo`
- `/gsd:health`

### Using Modified / Wrapped

| GSD Component | MDF Wrapper | What Changes |
|---------------|-------------|--------------|
| `/gsd:discuss-phase` | `/mdf:discuss-phase` | Replaced entirely by Phase Researcher; no user discussion |
| `/gsd:plan-phase` | `/mdf:plan-phase` | Phase Researcher produces model-aware CONTEXT.md as input |
| `/gsd:execute-phase` | `/mdf:execute-phase` | Guidelines Checker agent added per executor chunk |
| `/gsd:verify-work` | `/mdf:verify-work` | Cross-references implementation against model |
| `/gsd:complete-milestone` | `/mdf:complete-milestone` | Thin wrapper; preserves GSD behavior |
| `/gsd:new-milestone` | `/mdf:new-milestone` | Thin wrapper; preserves GSD behavior |
| CONTEXT.md format | Extended | Adds `<model_context>` section (which domains apply, pre-answered decisions, model gaps) |
| GUIDELINES.md | Extended scope | GSD treats as project conventions; MDF treats as engineering conventions refined from real code |
| `config.json` | Extended | Guidelines Checker agent added alongside existing workflow agents |
| CLAUDE.md injection | Extended | MDF appends model reference instructions so all GSD agents load model context automatically |

### Not Using

| GSD Component | Reason |
|---------------|--------|
| `/gsd:new-project` | Replaced by `/mdf:new-project` — bootstraps both `.planning/` and `.design/` |
| `gsd-phase-researcher` | Replaced by Phase Researcher — model-driven context gathering, no open-ended questioning |
| Phase 0–2 workflow | No GSD equivalent — entirely custom design and verification pipeline |

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Custom agents for Phase 0–2, GSD for Phase 3+ | Pre-implementation is user-discussion-heavy; GSD's plan/execute structure fits implementation, not design |
| Researcher replaces discuss-phase | Model provides pre-answered structural decisions; no need for open-ended user questioning per phase |
| GUIDELINES + TRANSLATION refined event-driven | Conventions emerge from seeing real code; scheduling refinement would be premature |
| Behavior docs at domain/class/state-machine granularity | Mirrors model structure for searchability; more granular scope takes precedence on conflict |
| Domain-verifier runs at end of each planning step | Catches inconsistencies before they propagate; does not produce an artifact |
| Model is never frozen | Implementation and testing may reveal model errors or scope changes; model-updater handles updates |
| Execution domain is metamodel, not model | Fixed contract across projects; TRANSLATION.md is the per-target implementation guide |
| Git submodule or parent directory for multi-repo | Keeps model central; orchestration across repos deferred to v2 |
| `/mdf` skill namespace | Model-Driven Framework — accurate, concise, not methodology-specific |
