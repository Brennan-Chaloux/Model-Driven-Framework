# Roadmap: Model-Driven Framework (MDF) v1.0

## Overview

Build the complete MDF toolchain in strict dependency order: schema and templates first (the contract everything else depends on), then MCP primitive tools from model I/O through Draw.io through simulation, then agent prompt files that call those tools, then skills that orchestrate the agents, and finally the integration skills that complete the Phase 0-2 workflow. Each layer is independently verifiable before the next begins.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Schema Foundation** - Define YAML model schema (Pydantic), canonical Draw.io bijection, and all artifact templates
- [ ] **Phase 2: MCP Server + model_io** - Scaffold the FastMCP server package and implement the three foundational CRUD tools
- [ ] **Phase 3: Validation Tool** - Implement validate_model with graph reachability, structural checks, and pycca pre-parser
- [ ] **Phase 4: Draw.io Tools** - Implement render_to_drawio, validate_drawio, and sync_from_drawio against the locked canonical schema
- [ ] **Phase 5: Simulation** - Implement simulate_state_machine with lark pycca parser and event-driven interpreter
- [ ] **Phase 6: Test Suite** - Build pytest suite covering all tools with round-trip integration test
- [ ] **Phase 7: Core Agents** - Write Domain Architect, Project Researcher, Class Diagram, State Diagram, and Domain Verifier agent prompts
- [ ] **Phase 8: Simulation and Execution Agents** - Write Simulation Test Generator and Execution Domain agent prompts
- [ ] **Phase 9: Core Skills** - Implement all Phase 0 skills from new-project through verify-model plus pause/resume
- [ ] **Phase 10: Integration Skills** - Implement configure-target and plan-roadmap to complete the Phase 0-2 workflow

## Phase Details

### Phase 1: Schema Foundation
**Goal**: Engineers and tools have a locked, versioned contract for every model element — YAML schema, Draw.io shape mappings, and scaffold templates
**Depends on**: Nothing (first phase)
**Requirements**: SCHEMA-01, SCHEMA-02, SCHEMA-03, SCHEMA-04, SCHEMA-05, TMPL-01, TMPL-02, TMPL-03, TMPL-04
**Success Criteria** (what must be TRUE):
  1. A valid domain YAML file (classes, associations, state machines, domain bridges) can be written by hand and accepted by the Pydantic schema without errors
  2. Every model element (class, association, state, transition, domain bridge) maps to exactly one Draw.io shape type — the bijection table is written and agreed upon
  3. The Draw.io round-trip test passes: a generated XML file opened and saved in real Draw.io produces a diff that the sync parser can handle without loss
  4. All artifact templates (DOMAINS.md, CLASS_DIAGRAM.yaml, STATE_DIAGRAM.yaml, behavior docs) exist and are populated with correct structure
  5. Any model YAML file that omits schema_version is rejected at schema validation time
**Plans**: TBD

### Phase 2: MCP Server + model_io
**Goal**: The mdf-server Python package is installable and the three foundational model I/O tools are functional
**Depends on**: Phase 1
**Requirements**: MCP-00, MCP-01, MCP-02, MCP-03
**Success Criteria** (what must be TRUE):
  1. Running `pip install -e ./mdf-server` succeeds and Claude can connect to the server via MCP protocol
  2. `list_domains()` returns domain names from `.design/model/` and returns an empty list when the directory does not exist
  3. `read_model(domain)` returns the YAML string for a known domain and an error listing available domains for an unknown one
  4. `write_model(domain, yaml)` saves a valid YAML file and returns a structured issue list for malformed input without throwing an exception
**Plans**: TBD

### Phase 3: Validation Tool
**Goal**: Structural model errors are caught automatically with actionable, location-specific issue lists — not pass/fail booleans
**Depends on**: Phase 2
**Requirements**: MCP-04
**Success Criteria** (what must be TRUE):
  1. `validate_model(domain)` returns a list of `{issue, location, value, fix}` objects — never raises an exception, never returns a boolean
  2. Unreachable states (states with no incoming transition from reachable states) are detected and reported with state name and domain location
  3. Trap states (states with no outgoing transitions) are detected and reported
  4. Referential integrity errors (association referencing a class that does not exist, transition targeting a state that does not exist) are reported with specific names
**Plans**: TBD

### Phase 4: Draw.io Tools
**Goal**: Engineers can generate, validate, and sync Draw.io diagrams from YAML with a deterministic, round-trip-stable workflow
**Depends on**: Phase 3
**Requirements**: MCP-05, MCP-06, MCP-07
**Success Criteria** (what must be TRUE):
  1. `render_to_drawio(domain)` produces XML that opens correctly in Draw.io with all classes, associations, states, and transitions visually present
  2. Calling `render_to_drawio` twice on the same unchanged YAML produces byte-identical output (idempotent)
  3. `validate_drawio(domain, xml)` returns an issue list for XML containing unrecognized shape types and returns an empty list for valid canonical XML
  4. `sync_from_drawio(domain, xml)` updates the YAML file from engineer-edited Draw.io XML and automatically runs `validate_model` — the returned issue list reflects post-sync structural state
**Plans**: TBD

### Phase 5: Simulation
**Goal**: Engineers can run event sequences against state machines and receive execution traces that verify behavioral correctness
**Depends on**: Phase 3
**Requirements**: MCP-08
**Success Criteria** (what must be TRUE):
  1. `simulate_state_machine(class, events)` processes an event sequence and returns a trace listing each `{event, from_state, to_state, guards_evaluated, actions_executed, final_state}` entry
  2. The lark grammar parses valid pycca action blocks (assignments, generate statements, bridge calls, conditionals) without error
  3. A guard condition that evaluates to false causes the transition to be skipped and that guard evaluation is visible in the trace
  4. An undefined class name or unparseable pycca block returns a structured error — not a Python exception propagating to the caller
**Plans**: TBD

### Phase 6: Test Suite
**Goal**: All MCP tools have automated coverage confirming correctness, regression safety, and round-trip fidelity
**Depends on**: Phase 5
**Requirements**: MCP-09
**Success Criteria** (what must be TRUE):
  1. `pytest mdf-server/tests/` passes with zero failures on a clean checkout
  2. `test_model_io.py` covers list/read/write for valid input, missing domain, and schema-invalid input
  3. `test_drawio_roundtrip.py` confirms that YAML → XML → sync → YAML preserves semantic equivalence (same classes, associations, and state topology)
  4. `test_validation.py` confirms that unreachable states, trap states, and broken referential integrity are each detected
  5. `test_simulation.py` confirms that a known event sequence on a known state machine produces the expected trace
**Plans**: TBD

### Phase 7: Core Agents
**Goal**: Agent prompt files exist for all domain-modeling roles and produce correct artifacts when spawned by skills
**Depends on**: Phase 2
**Requirements**: AGENT-01, AGENT-02, AGENT-03, AGENT-04, AGENT-05
**Success Criteria** (what must be TRUE):
  1. The Domain Architect agent, when spawned, asks structured domain boundary and bridge questions and writes a valid DOMAINS.md
  2. The Class Diagram Agent asks class, attribute, identifier, and association questions for a given domain and writes a schema-valid class diagram YAML
  3. The State Diagram Agent elicits states, transitions, guards, and pycca actions and writes a schema-valid state diagram YAML
  4. The Domain Verifier agent runs after each modeling step and returns either an empty issue list or a structured list — it never produces a narrative pass/fail verdict
  5. The Project Researcher agent extracts features, pitfalls, and stack information and writes research docs to `.design/research/`
**Plans**: TBD

### Phase 8: Simulation and Execution Agents
**Goal**: Behavioral verification and target scaffolding agents are functional and connect the model to execution
**Depends on**: Phase 7
**Requirements**: AGENT-06, AGENT-07
**Success Criteria** (what must be TRUE):
  1. The Simulation Test Generator, given behavior docs, derives test cases expressed as `(class, event_sequence, expected_trace)` tuples and calls `simulate_state_machine` for each
  2. The Simulation Test Generator reports pass or fail per behavioral spec with specific trace deviations cited — not summary counts
  3. The Execution Domain Agent generates an execution domain scaffold from metamodel rules and target specifications with minimal user input for target-specific decisions
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
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Schema Foundation | 0/TBD | Not started | - |
| 2. MCP Server + model_io | 0/TBD | Not started | - |
| 3. Validation Tool | 0/TBD | Not started | - |
| 4. Draw.io Tools | 0/TBD | Not started | - |
| 5. Simulation | 0/TBD | Not started | - |
| 6. Test Suite | 0/TBD | Not started | - |
| 7. Core Agents | 0/TBD | Not started | - |
| 8. Simulation and Execution Agents | 0/TBD | Not started | - |
| 9. Core Skills | 0/TBD | Not started | - |
| 10. Integration Skills | 0/TBD | Not started | - |

---
*Roadmap created: 2026-03-05 for milestone v1.0 Foundation*
