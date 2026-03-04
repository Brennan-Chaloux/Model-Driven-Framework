# Model-Based Project Framework

## What This Is

An MCP-based design workbench that adds an engineering design layer on top of GSD. It enables engineers to build and validate YAML domain models, Draw.io diagrams, and soft guidelines documents before any code is written — so that GSD's `execute-phase` produces exactly what the engineer expects, with no structural surprises mid-execution.

## Core Value

Engineers can verify the full structural design before typing `execute-phase` — no guessing, no mid-execution surprises.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] MCP server with tools for YAML model CRUD, Draw.io rendering, structural validation, and Draw.io sync
- [ ] YAML semantic model format aligned with xUML/Shlaer-Mellor methodology (classes, associations, state machines)
- [ ] Draw.io XML generation from YAML model (structural equality, not byte equality)
- [ ] Structural validation that produces actionable, per-issue error lists (not pass/fail)
- [ ] `/design:start` skill that conducts engineering-level domain questioning (classes, associations, state machines, interfaces)
- [ ] Soft guidelines document artifact — templated sections with escape hatch
- [ ] Design artifacts feed into GSD `discuss-phase` and `plan-phase` as enriched context
- [ ] C code generation target (embedded systems path)
- [ ] Python code generation target (simulation/test path)

### Out of Scope

- Modifying GSD files — GSD is updated periodically; all customizations live in skills and this MCP package
- Micca DSL / pycca compilation path for v1 — like-to-have, defer until models are validated against a real project
- State machine simulation (`simulate_state_machine`) for v1 — useful but not blocking
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
- **Skill structure**: Start with single `/design:start` skill; decompose into family if it gets unwieldy

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| MCP workbench over skills-only | Skills alone can't read/update .drawio after writing — design iteration is blind without MCP state | — Pending |
| YAML as source of truth (not Draw.io) | Claude generates and reasons about YAML reliably; Draw.io is a presentation view only | — Pending |
| Structural equality for Draw.io validation | Byte equality is too fragile — user moves shapes visually; validate semantics not layout | — Pending |
| Single `/design:start` skill to start | Ship one comprehensive skill first; decompose if it gets unwieldy | — Pending |
| Soft guidelines: template with escape hatch | Standard sections as defaults; any section skippable or addable | — Pending |

---
*Last updated: 2026-03-04 after initialization*
