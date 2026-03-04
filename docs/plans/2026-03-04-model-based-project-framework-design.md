# Model-Based Project Framework — Brainstorming Design Doc

**Date:** 2026-03-04
**Status:** Brainstorming complete — ready for /gsd:new-project

---

## Problem Statement

Three distinct problems motivate this project:

1. **Design fragility**: Code + tests are expensive to change. A design layer (diagrams, interfaces) that is cheap to iterate on should precede coding.
2. **Soft guidelines gap**: GSD captures hard acceptance criteria but misses the architectural intuitions, conventions, and patterns that shape *how* code is written. These cannot be extracted from requirements alone.
3. **Execution autonomy**: Plans should be detailed enough that Claude executes with minimal user decision-making mid-flight. The goal is that by the end of a planning phase, the code should essentially write itself.

---

## Chosen Approach: MCP-Driven Design Workbench

Build a design-first layer **on top of GSD** (without modifying GSD files, since GSD is updated periodically). The layer consists of:

- **Custom skills** for workflow orchestration (design conversations, iteration, GSD handoff)
- **MCP tools** in a new `model-based-project-framework` package for artifact management

Three approaches were considered:

| Approach | Description | Why Not |
|----------|-------------|---------|
| A — Skills only | Custom skills producing Draw.io + guidelines docs | Claude can't read/update .drawio files after writing them — design iteration is blind |
| **B — MCP Workbench** | Skills + MCP tools for model CRUD, rendering, validation | **Chosen** — persistent state, Claude can inspect and evolve the model across sessions |
| C — Design Milestone Wrapper | Skills wrapping GSD's milestone structure | Same blindness problem as A |

---

## Artifact Types

### 1. YAML Semantic Model (Source of Truth)
Claude's native working format. One file per domain subsystem. Structurally aligned with xUML/Shlaer-Mellor methodology (Leon Starr's work).

```yaml
domain: Motor Control System

classes:
  Motor:
    stereotype: entity
    attributes:
      id:         {type: int, identifier: true}
      speed:      {type: float, unit: rpm}
      is_running: {type: bool, default: false}
    methods:
      start:  {params: [{rpm: float}], returns: void}
      stop:   {params: [],             returns: void}
    state_machine:
      initial: Idle
      states: [Idle, Running, Fault]
      transitions:
        - {from: Idle,    to: Running, event: start, guard: "rpm > 0", action: "set_speed(rpm)"}
        - {from: Running, to: Idle,    event: stop,                    action: "set_speed(0)"}
        - {from: Running, to: Fault,   event: fault}

associations:
  - {from: Controller, to: Motor, multiplicity: "1..*", verb: controls, type: association}
```

**Why YAML over pycca/Micca DSL directly:**
- Claude can generate and reason about YAML reliably with small token footprint
- Semantics are obvious — no layout noise
- State machines are naturally expressible and interpretable
- xUML conventions (identifiers, stereotypes, verb phrases) map directly onto YAML keys
- One file per domain subsystem — Claude never needs to load the whole model

### 2. Draw.io XML (Presentation View)
Generated FROM the YAML model by an MCP tool. The user owns this visually — they can move shapes, add color, adjust layout. The system does not require byte-for-byte round-trip fidelity; it validates **structurally** (same connections, same classes, same relationships).

### 3. Soft Guidelines Document
A first-class document type capturing:
- Architectural patterns and principles
- Coding conventions and preferences
- Anti-patterns to avoid
- Technology choices and rationale
- Module/layer boundaries
- Non-functional requirements (performance, extensibility, etc.)

This is what GSD currently misses. It feeds into GSD as enriched context.

### 4. Interface Contracts
Class diagrams WITH method signatures — function names, parameter types, return types. Visual (Draw.io), derived from the YAML model. This is the "design down to function call" artifact.

---

## MCP Tool Design

| Tool | Purpose |
|------|---------|
| `read_model(domain)` | Returns YAML model for a domain |
| `write_model(domain, yaml)` | Saves and validates model |
| `render_to_drawio(domain)` | Converts YAML → Draw.io XML |
| `validate_model(domain)` | Checks consistency (referential integrity, undefined classes, etc.) |
| `sync_from_drawio(domain, drawio_xml)` | Extracts structural changes user made in Draw.io, merges back to YAML |
| `list_domains()` | Lists all domain models in the project |
| `simulate_state_machine(class, events)` | *(like-to-have)* Runs state machine against event sequence, returns trace |

### Validation Layer (YAML ↔ Draw.io)
When the user edits a Draw.io file visually, structural equality is checked — not byte equality. Two representations are equal if:
- Same set of classes
- Same attributes and method signatures per class
- Same associations (same endpoints, multiplicity, verb phrase)
- Same state machine topology (states and transitions, ignoring layout/style)

---

## xUML / Model-Based Design Alignment

The project adopts **Shlaer-Mellor Executable UML** methodology:
- Already in use at Dilon Technologies (PlantUML style guide uses xUML conventions)
- Dilon's PlantUML guide covers: class identification ({I}, {I2}, {R#}), verb phrase relationships, state machines — all map to this YAML schema

**Key references:**
- *Models to Code* (Starr, Mangogna, Mellor — Apress 2017)
- Leon Starr's modelint GitHub: https://github.com/modelint
- Micca / pycca model compilers: http://repos.modelrealization.com
- Scrall action language: https://github.com/modelint/scrall

**Micca vs pycca:**
- pycca: Tcl-based, targets embedded microcontrollers via STSA, well-documented syntax
- Micca: C-based, more modern, multi-platform (POSIX, EFM32GG, MSP432, MSP430)
- Both share the same xUML domain/class/state-machine conceptual model
- Micca DSL is not fully public-facing (locked in Fossil literate docs)

**Like-to-have:** YAML model → Micca DSL translation MCP tool, enabling actual model compilation and behavioral simulation before writing embedded C code.

---

## Integration with GSD

The design phase produces artifacts that feed GSD as richly detailed inputs:

```
/design:start              ← New workflow (custom skill)
  → Soft guidelines doc    ← Fills the GSD "soft guidelines gap"
  → Domain YAML models     ← Claude's working representation
  → Draw.io class diagrams ← Visual review / stakeholder communication
  → Interface contracts    ← Method signatures locked before coding
        ↓
/gsd:new-project           ← Consumes above as PROJECT.md + REQUIREMENTS.md
/gsd:plan-phase            ← Consumes YAML models as detailed CONTEXT.md
/gsd:execute-phase         ← Nearly autonomous — design decisions already made
```

Key principle: **Build on top of GSD, never modify GSD.** GSD is updated periodically; customizations live in skills and this MCP package.

---

## Embedded Systems Considerations

The execution domain needs flexibility:
- YAML model is platform-independent
- Code generation targets are configurable (C for embedded, Python for simulation, etc.)
- State machine simulation enables behavioral debugging before hardware is available
- Model compiler path (→ Micca DSL → C) is a like-to-have, not a hard requirement

---

## Open Questions for /gsd:new-project Session

1. What is the first concrete project this framework will be used on? (Helps validate the design with a real use case)
2. Should the MCP tools live in a standalone package or be added to `dilon-claude-tools`?
3. What is the target language for code generation from the model? (C for embedded, Python for tests/simulation, both?)
4. How should the soft guidelines document be structured — freeform or templated sections?
5. Should `/design:start` be a single comprehensive skill or a family of composable skills (e.g., `/design:domain`, `/design:state-machine`, `/design:approve`)?
