# Requirements: Model-Driven Framework (MDF)

**Defined:** 2026-03-05
**Core Value:** Engineers can verify the full structural design before typing `execute-phase` — no guessing, no mid-execution surprises.

## v1.0 Requirements

### Schema Foundation

- [ ] **SCHEMA-01**: YAML model schema defined — classes (stereotypes, identifiers, attributes, methods), associations (verb phrase, multiplicity), state machines (states, transitions, guards, pycca actions), domain bridges (from/to, operation, params, direction)
- [ ] **SCHEMA-02**: `schema_version` field required in all model files from day one
- [ ] **SCHEMA-03**: Canonical Draw.io schema defined — 1:1 bijection with YAML; canonical shape-type-per-element table locked; no freeform shapes without YAML equivalent
- [ ] **SCHEMA-04**: Draw.io round-trip test passes — generate XML, open in real Draw.io, save, sync back; structural equality confirmed before any tool is built
- [ ] **SCHEMA-05**: Behavior doc format defined — domain-level, class-level, and state-machine-level templates

### Templates

- [ ] **TMPL-01**: `DOMAINS.md` template — domain map with realized domains and bridge index
- [ ] **TMPL-02**: `CLASS_DIAGRAM.yaml` template — class diagram YAML scaffold
- [ ] **TMPL-03**: `STATE_DIAGRAM.yaml` template — state diagram YAML scaffold
- [ ] **TMPL-04**: Behavior doc templates — `behavior-domain.md`, `behavior-class.md`, `behavior-state.md`

### MCP Server

- [ ] **MCP-00**: MCP server package scaffolded — `mdf-server/` with `pyproject.toml`, `server.py`, module structure (`tools/`, `schema/`, `pycca/`)
- [ ] **MCP-01**: `list_domains()` — returns all domain names in `.design/model/`
- [ ] **MCP-02**: `read_model(domain)` — returns YAML for one domain; error if not found lists available domains
- [ ] **MCP-03**: `write_model(domain, yaml)` — saves, validates against schema, returns issue list; idempotent
- [ ] **MCP-04**: `validate_model(domain)` — returns list of issues: referential integrity, graph reachability (BFS/DFS unreachable states, trap states), pycca syntax pre-check; never pass/fail
- [ ] **MCP-05**: `render_to_drawio(domain)` — generates Draw.io XML from YAML per canonical schema; deterministic and idempotent
- [ ] **MCP-06**: `validate_drawio(domain, xml)` — validates Draw.io XML against canonical schema before sync; returns issue list
- [ ] **MCP-07**: `sync_from_drawio(domain, xml)` — structured schema-aware parse back to YAML; runs `validate_model` automatically; returns issue list
- [ ] **MCP-08**: `simulate_state_machine(class, events)` — runs pycca event sequence, returns execution trace (state transitions, guards evaluated, actions executed, final state)
- [ ] **MCP-09**: Test suite — `test_model_io`, `test_drawio_roundtrip`, `test_validation`, `test_simulation`

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

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| SCHEMA-01 | Phase 1 | Pending |
| SCHEMA-02 | Phase 1 | Pending |
| SCHEMA-03 | Phase 1 | Pending |
| SCHEMA-04 | Phase 1 | Pending |
| SCHEMA-05 | Phase 1 | Pending |
| TMPL-01 | Phase 1 | Pending |
| TMPL-02 | Phase 1 | Pending |
| TMPL-03 | Phase 1 | Pending |
| TMPL-04 | Phase 1 | Pending |
| MCP-00 | Phase 2 | Pending |
| MCP-01 | Phase 2 | Pending |
| MCP-02 | Phase 2 | Pending |
| MCP-03 | Phase 2 | Pending |
| MCP-04 | Phase 3 | Pending |
| MCP-05 | Phase 4 | Pending |
| MCP-06 | Phase 4 | Pending |
| MCP-07 | Phase 4 | Pending |
| MCP-08 | Phase 5 | Pending |
| MCP-09 | Phase 6 | Pending |
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
- v1.0 requirements: 41 total
- Mapped to phases: 36
- Unmapped: 0 ✓

---
*Requirements defined: 2026-03-05*
*Last updated: 2026-03-05 — traceability updated to match 10-phase roadmap*
