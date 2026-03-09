# Roadmap: MDF Server (mdf-server) v1.0

## Overview

Build the Claude interface layer for MDF: agent prompt files, modeling reference documents, and Phase 0 skills that orchestrate those agents. Schema, MCP tools, and simulation engine are implemented in the mdf-simulator repository and consumed here via the `mdf-sim/` submodule. Each layer is independently verifiable before the next begins.

## Phases

**Phase Numbering:**
- Integer phases (7, 8, 9, 10): Planned milestone work owned by mdf-server
- Phases 1–6 are implemented in the mdf-simulator repository

- [x] **Phases 1–6: Schema + Tools** — Implemented in mdf-simulator repository
- [ ] **Phase 7: Core Agents + Modeling References** - Write Domain Architect, Project Researcher, Class Diagram, State Diagram, and Domain Verifier agent prompts; write domains, classes, state machines, and bridges reference files
- [ ] **Phase 8: Simulation and Execution Agents** - Write Simulation Test Generator and Execution Domain agent prompts; write execution domain reference file
- [ ] **Phase 9: Core Skills** - Implement all Phase 0 skills from new-project through verify-model plus pause/resume
- [ ] **Phase 10: Integration Skills** - Implement configure-target and plan-roadmap to complete the Phase 0-2 workflow

## Phase Details

### Phase 7: Core Agents + Modeling References
**Goal**: Agent prompt files exist for all domain-modeling roles and produce correct artifacts when spawned by skills; xUML modeling reference files are available for Claude agents to load during domain, class, and bridge work
**Depends on**: mdf-sim submodule (model_io tools available)
**Requirements**: AGENT-01, AGENT-02, AGENT-03, AGENT-04, AGENT-05, REF-01, REF-02, REF-03, REF-04
**Success Criteria** (what must be TRUE):
  1. The Domain Architect agent, when spawned, asks structured domain boundary and bridge questions and writes a valid DOMAINS.md
  2. The Class Diagram Agent asks class, attribute, identifier, and association questions for a given domain and writes a schema-valid class diagram YAML
  3. The State Diagram Agent elicits states, transitions, guards, and pycca actions and writes a schema-valid state diagram YAML
  4. The Domain Verifier agent runs after each modeling step and returns either an empty issue list or a structured list — it never produces a narrative pass/fail verdict
  5. The Project Researcher agent extracts features, pitfalls, and stack information and writes research docs to `.design/research/`
  6. Reference files exist at `references/domains-reference.md`, `references/classes-reference.md`, `references/state-machines-reference.md`, and `references/bridges-reference.md` and contain actionable xUML heuristics
**Plans**: TBD

### Phase 8: Simulation and Execution Agents
**Goal**: Behavioral verification and target scaffolding agents are functional and connect the model to execution; execution domain reference file is available for the Execution Domain Agent
**Depends on**: Phase 7
**Requirements**: AGENT-06, AGENT-07, REF-05
**Success Criteria** (what must be TRUE):
  1. The Simulation Test Generator, given behavior docs, derives test cases expressed as `(class, event_sequence, expected_trace)` tuples and calls `simulate_state_machine` for each
  2. The Simulation Test Generator reports pass or fail per behavioral spec with specific trace deviations cited — not summary counts
  3. The Execution Domain Agent generates an execution domain scaffold from metamodel rules and target specifications with minimal user input for target-specific decisions
  4. `references/execution-domain-reference.md` exists with metamodel execution rules, required contracts, and recommended starting points for a new target
**Plans**: TBD

### Phase 9: Core Skills
**Goal**: Engineers can run the complete Phase 0 design workflow — from new project to verified model — in a resumable, session-safe way
**Depends on**: Phase 8
**Requirements**: SKILL-01, SKILL-02, SKILL-03, SKILL-04, SKILL-05, SKILL-06, SKILL-07, SKILL-08
**Success Criteria** (what must be TRUE):
  1. `/mdf:new-project` creates the `.planning/` and `.design/` directory structures, copies all templates, and appends the model reference block to CLAUDE.md in one invocation
  2. `/mdf:pause` commits session state to git and writes a session-summary artifact that a subsequent `/mdf:resume` can read to reconstruct stage, domain in progress, and open decisions
  3. `/mdf:resume` calls `list_domains()`, reads the session summary, and presents the next action without requiring user re-explanation of current state
  4. The discuss-domain → discuss-class → discuss-state → review-model → verify-model sequence can be run end-to-end on a single domain, producing validated YAML and a passed simulation test suite
  5. `/mdf:review-model` renders Draw.io for all domains and correctly routes through validate_drawio + sync_from_drawio after engineer edits, then surfaces any resulting validation issues
**Plans**: TBD

### Phase 10: Integration Skills
**Goal**: Engineers can configure a build target and generate a GSD-compatible roadmap from a completed model, completing the Phase 0-2 handoff to GSD
**Depends on**: Phase 9
**Requirements**: SKILL-09, SKILL-10
**Success Criteria** (what must be TRUE):
  1. `/mdf:configure-target` updates STACK.md, generates TRANSLATION.md, and scaffolds the execution domain via the Execution Domain Agent in a single skill invocation
  2. `/mdf:plan-roadmap` reads the completed model and produces a valid GSD ROADMAP.md and MILESTONES.md that the standard GSD executor can consume without modification
  3. The generated GSD ROADMAP.md contains phase goals and success criteria derived from model domains and domain bridges — not generic placeholders
**Plans**: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 7 → 8 → 9 → 10

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 7. Core Agents | 0/TBD | Not started | - |
| 8. Simulation and Execution Agents | 0/TBD | Not started | - |
| 9. Core Skills | 0/TBD | Not started | - |
| 10. Integration Skills | 0/TBD | Not started | - |

---
*Roadmap created: 2026-03-05 for milestone v1.0 Foundation*
*Last updated: 2026-03-09 — Repo split; Phases 1–6 moved to mdf-simulator; mdf-server roadmap starts at Phase 7*
