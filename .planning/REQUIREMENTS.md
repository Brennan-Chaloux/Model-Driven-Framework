# Requirements: MDF Server (mdf-server) — Claude Interface

**Defined:** 2026-03-05
**Updated:** 2026-03-09 — Repo split applied
**Core Value:** Engineers can verify the full structural design before typing `execute-phase` — no guessing, no mid-execution surprises.

> **Note:** MCP tool requirements (MCP-00..MCP-09) and schema/template requirements (SCHEMA-*, TMPL-*) are tracked in the mdf-simulator repository. This file covers only the requirements owned by mdf-server: agents, skills, and modeling reference files.

## v1.0 Requirements

### Modeling Reference Files

- [ ] **REF-01**: `references/domains-reference.md` — domain identification rules, system responsibility decomposition, realized domain recognition, bridge definition heuristics; loaded by `/mdf:discuss-domain`
- [ ] **REF-02**: `references/classes-reference.md` — class identification, stereotypes (entity/associative/active), identifier selection, class vs attribute distinction; loaded by `/mdf:discuss-class`
- [ ] **REF-03**: `references/state-machines-reference.md` — which classes need state machines, state identification, transition guard rules, action language heuristics; loaded by `/mdf:discuss-state`
- [ ] **REF-04**: `references/bridges-reference.md` — bridge operation definition, required vs provided direction, what belongs in a bridge vs inside a domain; loaded by `/mdf:discuss-domain` and `/mdf:discuss-class`
- [ ] **REF-05**: `references/execution-domain-reference.md` — metamodel execution domain rules and required contracts, recommended starting points for a new target; loaded by `/mdf:configure-target` and Execution Domain Agent

### Agents

- [ ] **AGENT-01**: Domain Architect — extracts domain map, boundaries, realized domains, bridges through conversation → writes DOMAINS.md
- [ ] **AGENT-02**: Project Researcher — extracts features, pitfalls, stack → writes `.design/research/` docs
- [ ] **AGENT-03**: Class Diagram Agent — extracts class structure per domain through questioning → writes class diagram YAML + class behavior docs
- [ ] **AGENT-04**: State Diagram Agent — extracts state machine structure through questioning → writes state diagram YAML + state machine behavior docs
- [ ] **AGENT-05**: Domain Verifier — consistency checker; runs at end of each planning step; reports pass or issue list to calling agent; no artifact
- [ ] **AGENT-06**: Simulation Test Generator — reads behavior docs → derives test cases from realized bridge inputs → calls `simulate_state_machine` per test → reports pass/fail per behavioral spec
- [ ] **AGENT-07**: Execution Domain Agent — generates execution domain implementation from metamodel rules + target specs; minimal user input for target-specific decisions

### Phase 0–2 Skills

- [ ] **SKILL-01**: `/mdf:new-project` — bootstraps `.planning/` and `.design/` structure; copies templates; appends model reference block to `CLAUDE.md`; kicks off domain questioning
- [ ] **SKILL-02**: `/mdf:pause` — commits session state to git with checkpoint message; writes session-summary artifact (current stage, domain in progress, open decisions)
- [ ] **SKILL-03**: `/mdf:resume` — reads session-summary; calls `list_domains()`; reconstructs current stage and presents next action
- [ ] **SKILL-04**: `/mdf:discuss-domain` — multi-session domain questioning; spawns Domain Architect + Project Researcher + Domain Verifier at end of step; outputs DOMAINS.md + initial behavior docs
- [ ] **SKILL-05**: `/mdf:discuss-class` — class diagram planning per domain; spawns Class Diagram Agent + Domain Verifier at end of step; outputs class diagram YAML + class behavior docs
- [ ] **SKILL-06**: `/mdf:discuss-state` — state diagram planning per domain; spawns State Diagram Agent + Domain Verifier at end of step; outputs state diagram YAML + state machine behavior docs
- [ ] **SKILL-07**: `/mdf:review-model` — calls `render_to_drawio` for all domains; prompts engineer for visual review in Draw.io; handles `validate_drawio` + `sync_from_drawio` after engineer edits
- [ ] **SKILL-08**: `/mdf:verify-model` — spawns Simulation Test Generator; runs test suite; reports pass/fail per behavioral spec; Domain Verifier runs full-model consistency check
- [ ] **SKILL-09**: `/mdf:configure-target` — updates STACK.md; generates TRANSLATION.md; scaffolds execution domain via Execution Domain Agent; initializes target repo(s)
- [ ] **SKILL-10**: `/mdf:plan-roadmap` — generates GSD ROADMAP.md + MILESTONES.md from completed model for Phase 3+ implementation phases

## v2 Requirements

### Reference Files

- **REF-06**: `references/translation-reference.md` — how to map model action language to target-specific code patterns; loaded by Phase Researcher and `/mdf:configure-target`

### Phase 3+ Skills

- `/mdf:discuss-phase` — model-aware CONTEXT.md (replaces GSD discuss-phase)
- `/mdf:plan-phase` — model-aware planner wrapper
- `/mdf:execute-phase` — GSD executor + Guidelines Checker per chunk
- `/mdf:verify-work` — GSD verifier + model conformance check
- `/mdf:complete-milestone` — thin GSD wrapper
- `/mdf:new-milestone` — thin GSD wrapper
- `/mdf:update-model` — reactive model corrections and scope changes

### Phase 3+ Agents

- Phase Researcher — reads model + TRANSLATION.md → CONTEXT.md; refines GUIDELINES + TRANSLATION
- Guidelines Checker — runs per executor chunk against GUIDELINES.md
- Model Updater — reactive agent for model corrections and scope changes

## Out of Scope

| Feature | Reason |
|---------|--------|
| Modifying GSD files | GSD updated periodically; all customizations in skills and MCP package |
| Micca as compilation target | pycca chosen; Micca deferred |
| Multi-user collaboration | Single engineer context for now |
| Multi-target orchestration | Deferred to v3+; single-target or manual multi-target for now |
| Scrall action language | Less mature tooling for C targets; evaluate after pycca path proven |
| Schema, MCP tools, simulation | Tracked in mdf-simulator; mdf-server consumes them via mdf-sim submodule |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| REF-01 | Phase 7 | Pending |
| REF-02 | Phase 7 | Pending |
| REF-03 | Phase 7 | Pending |
| REF-04 | Phase 7 | Pending |
| REF-05 | Phase 8 | Pending |
| AGENT-01 | Phase 7 | Pending |
| AGENT-02 | Phase 7 | Pending |
| AGENT-03 | Phase 7 | Pending |
| AGENT-04 | Phase 7 | Pending |
| AGENT-05 | Phase 7 | Pending |
| AGENT-06 | Phase 8 | Pending |
| AGENT-07 | Phase 8 | Pending |
| SKILL-01 | Phase 9 | Pending |
| SKILL-02 | Phase 9 | Pending |
| SKILL-03 | Phase 9 | Pending |
| SKILL-04 | Phase 9 | Pending |
| SKILL-05 | Phase 9 | Pending |
| SKILL-06 | Phase 9 | Pending |
| SKILL-07 | Phase 9 | Pending |
| SKILL-08 | Phase 9 | Pending |
| SKILL-09 | Phase 10 | Pending |
| SKILL-10 | Phase 10 | Pending |

**Coverage:**
- v1.0 requirements owned by mdf-server: 22 total
- Mapped to phases: 22
- Unmapped: 0 ✓

---
*Requirements defined: 2026-03-05*
*Last updated: 2026-03-09 — Repo split; MCP/schema/template requirements moved to mdf-simulator*
