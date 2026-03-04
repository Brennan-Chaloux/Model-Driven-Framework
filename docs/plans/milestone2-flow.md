# Milestone 2: Code Generation from Model — Design Document

**Date:** 2026-03-04
**Status:** In progress — design conversation

**Pre-condition:** YAML domain models and `.design/GUIDELINES.md` exist (Milestone 1 complete).

---

## Overview

Milestone 2 is the GSD pipeline consuming the model artifacts produced in Milestone 1. The goal is that every GSD agent operates with the model as authoritative — structural decisions are pre-made, agents implement rather than design.

Standard GSD is not modified. Custom skills and agents wrap or replace specific steps where the model changes agent responsibilities.

---

## Flow

```
.design/models/          ← YAML models (Milestone 1 output)
.design/GUIDELINES.md    ← Engineering guidelines (Milestone 1 output)
        ↓
/design:discuss-phase N  ← Custom skill (replaces /gsd:discuss-phase)
        ↓ CONTEXT.md (with <model_context>)
/design:plan-phase N     ← Custom orchestrator (wraps /gsd:plan-phase)
  → custom researcher    ← Different research brief
  → gsd-planner          ← Same agent, model-aware prompt
  → gsd-plan-checker     ← Same agent, model conformance added
        ↓ PLAN.md
/gsd:execute-phase N     ← Standard GSD (reads CLAUDE.md → loads models)
  → gsd-executor         ← Same agent
  → guidelines-checker   ← New agent, runs per executor chunk
        ↓
/gsd:verify-work N       ← Standard GSD
```

---

## CLAUDE.md Injection

`/design:start` appends to the project root `CLAUDE.md`:

```markdown
## Design Models (model-based-project-framework)

Before planning or executing any phase, read the relevant domain models
from `.design/models/`. Implementation MUST conform to the YAML model —
class structure, state machines, and action language are authoritative.

See `.design/GUIDELINES.md` for engineering conventions that apply to
all implementation work.
```

This is picked up automatically by: gsd-planner, gsd-phase-researcher,
gsd-plan-checker, gsd-executor, and any agent that reads CLAUDE.md.

---

## Agent Analysis

### `/design:discuss-phase` (custom skill — replaces `/gsd:discuss-phase`)

**Inputs:**
- `ROADMAP.md` — phase goal, requirement IDs
- `PROJECT.md` — vision, constraints
- `REQUIREMENTS.md` — acceptance criteria
- `STATE.md` — current progress
- Prior `CONTEXT.md` files — decisions from earlier phases
- `.design/models/` — YAML domain models (new)
- `.design/GUIDELINES.md` — engineering conventions (new)
- Codebase scan — reusable assets, patterns, integration points

**Processing (different from standard discuss-phase):**
- Standard: "What do you want? Here are the implementation choices."
- Model-based: "Here's what the model specifies for this phase. Is it correct? What gaps remain?"
- Surfaces model coverage for the phase — presents pre-answered decisions
- Identifies model gaps (timing constraints, hardware specifics, edge cases, priorities)
- Validates model correctness and completeness for this phase's scope
- Creative control is heavily restricted — structural decisions are locked

**Outputs:**
- `CONTEXT.md` — same file location, extended contract:
  - `<model_context>` — which domains apply, file references, what's pre-answered vs gap (new section)
  - `<decisions>` — only model gaps captured here (narrowed scope)
  - `<code_context>` — reusable assets from codebase scan (unchanged)
  - `<specifics>` — phase-specific references (unchanged)
  - `<deferred>` — out-of-scope ideas preserved (unchanged)
- `STATE.md` update (unchanged)
- Git commit (unchanged)

**Note:** `<decisions>` contract changes. Standard discuss-phase populates it with
user preferences from conversation. Model-based version populates it only with
what the model does NOT cover. Most decisions are pre-answered in `<model_context>`.

---

### Custom Researcher (via `/design:plan-phase` orchestrator)

**Inputs:**
- `CONTEXT.md` (with `<model_context>`) — phase context including model references
- `REQUIREMENTS.md`
- `STATE.md`
- `CLAUDE.md` — model reference instructions
- `.design/models/` — YAML models (loaded per CLAUDE.md instruction)
- Phase description and requirement IDs
- Web search / Context7

**Research brief (different from standard):**
- Standard: "What do I need to know to PLAN this phase?" (includes structure)
- Model-based: "How do we implement what the model specifies on this target?"

**Research focuses on:**
- pycca action language implementation specifics for this phase's classes
- Platform/compiler constraints for target (embedded C, Python simulation)
- Testing approaches for model-generated code
- Integration patterns between domains (bridge implementation)
- Gotchas specific to implementing this model on this target
- For code generation phases: YAML → pycca DSL pipeline specifics

**Outputs:**
- `RESEARCH.md` — same format, different content focus
  - Implementation guidance for pre-defined structure (not structure recommendations)
  - Validation Architecture section (unchanged — still needed for Nyquist)

---

### `/design:plan-phase` Orchestrator (custom — wraps gsd-planner)

**What changes from standard plan-phase:**
- Researcher receives model-aware brief (above)
- Planner receives model-aware prompt:
  - "Structural decisions are pre-made in the YAML model — treat as authoritative"
  - "Reference model specs explicitly in every task description"
  - "Add model conformance to must_haves"
  - For code gen phases: use compiler pipeline task template instead of implementation template

**Inputs (same files, richer content):**
- `CONTEXT.md` (with `<model_context>`)
- `RESEARCH.md` (implementation-focused)
- `STATE.md`, `ROADMAP.md`, `REQUIREMENTS.md`
- `CLAUDE.md`

**Agent used:** `gsd-planner` (unchanged) — same agent, different brief from orchestrator

**Outputs — PLAN.md (same format, richer content):**
- Task descriptions reference specific model elements (class names, method signatures, state machine transitions)
- `must_haves` include model conformance checks:
  - "All classes in phase implement methods specified in YAML model"
  - "State machine topology matches model — all states reachable"
- Wave structure may reflect domain dependency order (domain bridges)

---

### Guidelines Checker (new agent — runs at executor level)

**When:** After each gsd-executor completes a task chunk (same wave, same pass as other code quality agents)

**Inputs:**
- Executor output — the code chunk just written
- `.design/GUIDELINES.md` — engineering conventions

**Processing (plan-checker pattern applied to guidelines):**
- Reviews code against each guideline section
- Produces per-issue list (not pass/fail)

**Outputs:**
- Conformance report: list of violations with location and fix guidance
- Integrated into execute-phase wave reporting

**Configuration:** Added to `config.json` alongside other workflow agents

---

### Standard Agents (unchanged)

- `gsd-executor` — reads CLAUDE.md → loads models → implements per model spec
- `gsd-plan-checker` — reads CLAUDE.md → verifies plans conform to model
- `gsd-verifier` — reads CLAUDE.md → cross-references implementation against model

---

## Open Questions

1. `/design:discuss-phase` — pre-step that hands off to standard discuss-phase, or full replacement?
2. `/design:plan-phase` — wrapper that modifies the brief, or full replacement orchestrator?
3. For code generation phases — what does the pycca compiler pipeline task template look like?
4. Guidelines checker — standalone agent type or integrated into gsd-executor as a post-step?

---

*Last updated: 2026-03-04 — Milestone 2 agent analysis*
