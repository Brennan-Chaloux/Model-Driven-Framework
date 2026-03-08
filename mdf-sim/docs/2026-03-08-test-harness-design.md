# MDF Simulation Test Harness Design

**Date:** 2026-03-08
**Status:** In Progress
**Scope:** CLI test harness — test file format, execution model, assertions

---

## Overview

`mdf-sim-test` is the CLI test harness for validating xUML domain models built with MDF. It runs the simulation engine against structured YAML test files and reports pass/fail per test. It exits with non-zero status on any failure.

Two complementary capabilities:

1. **Test runner** — executes test files against the simulation engine, evaluates trace assertions
2. **Model linter** — static analysis pass on the domain model, plugged into `validate_model` as an additional parameter

---

## Test Types

### Unit Tests (Class Tests)

Focused on a single class state machine in isolation. Other classes within the domain may exist in the fixture (for relationship traversal) but their state machines are inactive — events dispatched to them are logged but not processed.

### Integration Tests (Domain Tests)

Test emergent behavior between multiple collaborating classes. The fixture defines the minimum set of class instances needed for the scenario. The scope declares which state machines are active.

**File organization:**

```
tests/
  unit/
    valve.yaml
    sensor.yaml
    controller.yaml
  integration/
    valve_open_sequence.yaml
    emergency_shutdown.yaml
    sensor_calibration.yaml
```

The fixture bounds the scope of an integration test file — a file covers one coherent scenario involving a specific cluster of classes. This limits file size without eliminating large files for genuinely complex scenarios.

---

## Execution Model

For each test in a file:

1. Reset engine to clean state
2. Instantiate fixture (instances + relationships)
3. Register mocks (file-level, with per-test overrides applied)
4. Execute script steps in order (inject events, advance clock)
5. Run engine until `end_state` is reached or engine halts
6. Evaluate trace assertions against captured micro-step log
7. Report pass/fail with halt state and queue contents

If the engine halts before `end_state` is reached, the test fails. The harness reports which instances are in which states and what remains in the queues — this makes it visible whether the halt was at a senescent state, a wait state, or an unexpected deadlock.

---

## State Types

The engine and harness are aware of three state classifications:

| Type | Definition | Engine behavior |
|---|---|---|
| **Transient** | Entry actions always generate an event to self (unconditionally, or all branches of any conditional do so) | Immediately self-transitions; never a valid `end_state` |
| **Senescent** | No self-generate; instance is stable until external input | Engine halting here is expected and correct |
| **Wait state** | No self-generate; instance is waiting for a response to an event it already dispatched outward | Indistinguishable from senescent at runtime; scope configuration implicitly determines whether the response arrives |

The `end_state` declared in a test is validated at parse time — if the declared state is transient, the test fails immediately with an authoring error.

---

## Model Linter

Added as a validation pass to `validate_model`.

**State type consistency rule:** A state must be unambiguously transient or non-transient. The linter flags any state where a self-generate is conditional without a guaranteed else — meaning some code paths generate to self and others do not.

| Pattern | Valid |
|---|---|
| Unconditional `generate X to self` | ✓ Transient |
| All branches of if/else generate to self | ✓ Transient |
| No self-generate on any path | ✓ Senescent/Wait |
| Some branches generate to self, others do not | ✗ Flag — ambiguous |

---

## Test File Format

### Top-Level Structure

```yaml
domain: string          # domain to load and simulate
scope: [ClassName, ...] # state machines that are active; others are logged but not processed
mocks: ...              # bridge mock declarations (file-level)
fixture: [...]          # shared starting world — reset before each test
tests: [...]            # list of tests
```

### Mocks

Bridge operations are mocked before the engine runs. Mocks are declared at file level and can be overridden per test.

```yaml
mocks:
  ClassName.operation: value                  # static — always returns this value

  ClassName.operation:
    returns: [v1, v2, v3]                     # sequential — consumed in order per call
    on_exhaust: fail | repeat_last            # behavior when values are exhausted
```

**Senescence detection:** The harness tracks call counts against declared return values. If `on_exhaust: fail` (the default), calling an exhausted mock fails the test immediately with a clear error indicating the operation name and call count. This catches both bugs in the model (unexpected extra calls) and gaps in the test (insufficient values declared).

### Fixture

Declarative world state shared across all tests in the file. The engine resets to this exact state before every test.

```yaml
fixture:
  - instance:
      class: string
      id: string          # identifier attribute value
      state: string       # starting state (must be non-transient)
      attrs:
        attr_name: value

  - relate:
      class: string
      id: string
      rel: string         # relationship name (e.g. R1)
      to_class: string
      to_instance: string
```

No per-test instance additions. The fixture is the complete starting world. If a test's script causes new instances to be created as a side effect, those appear in the trace as `instance_created` assertions.

### Test Structure

```yaml
tests:
  - name: string

    mocks:                          # optional — overrides file-level mocks for this test only
      ClassName.operation: value

    script:
      - inject:
          class: string
          instance: string
          event: string
          args: {key: value}        # optional

      - tick: 500ms                 # advance simulated clock

    end_state:
      class: string
      instance: string
      state: string                 # validated as non-transient at parse time

    trace: [...]                    # ordered micro-step assertions and state checks
```

---

## Trace Assertions

The trace is an ordered sequence. The harness matches the captured micro-step log against the declared trace exactly — every step must match in order with no extras between assertions. A `check` assertion pauses evaluation and inspects world state at that point before continuing.

### Micro-Step Assertions

```yaml
- transition_fired:
    class: string
    instance: string
    from: string
    to: string

- action_executed:
    class: string
    instance: string
    assigns:
      attr_name: value

- generate_dispatched:
    event: string
    from_instance: string
    to_class: string
    to_instance: string
    queue: priority | standard
    args: {key: value}              # optional

- guard_evaluated:
    class: string
    instance: string
    expression: string
    result: true | false

- bridge_called:
    operation: string
    args: {key: value}
    returns: value

- event_delayed:
    event: string
    from_instance: string
    to_instance: string
    delay: 500ms

- event_delay_expired:
    event: string
    from_instance: string
    to_instance: string

- instance_created:
    class: string
    instance: string

- instance_deleted:
    class: string
    instance: string
```

### State Check Assertions

Interspersed within the trace at any point. Evaluated against live engine state at that position in the sequence.

```yaml
# Check an attribute value on an instance
- check:
    class: string
    instance: string
    attr: string
    eq: value

# Check whether a relationship instance exists
- check:
    class: string
    instance: string
    rel: string
    to_class: string
    to_instance: string
    exists: true | false

# Traverse a relationship and check an attribute on the result
- check:
    traverse: "ClassName[id].R1.TargetClass"
    attr: string
    eq: value
```

---

## Complete Example

```yaml
domain: valve_control

scope: [Valve]

mocks:
  Pressure.read_sensor:
    returns: [50.0, 110.0]
    on_exhaust: fail
  HMI.signal_open: true

fixture:
  - instance:
      class: Valve
      id: inlet
      state: Closed
      attrs:
        flow_rate: 0
  - instance:
      class: Sensor
      id: s1
      state: Idle
      attrs:
        reading: 0.0
  - relate:
      class: Valve
      id: inlet
      rel: R1
      to_class: Sensor
      to_instance: s1

tests:
  - name: open valve passes through pressurizing transient state
    script:
      - inject:
          class: Valve
          instance: inlet
          event: Open
    end_state:
      class: Valve
      instance: inlet
      state: Open
    trace:
      - transition_fired:
          class: Valve
          instance: inlet
          from: Closed
          to: Pressurizing
      - bridge_called:
          operation: Pressure.read_sensor
          returns: 50.0
      - action_executed:
          class: Valve
          instance: inlet
          assigns:
            flow_rate: 50
      - check:
          traverse: "Valve[inlet].R1.Sensor"
          attr: reading
          eq: 0.0
      - generate_dispatched:
          event: PressureReached
          from_instance: inlet
          to_instance: inlet
          queue: priority
      - transition_fired:
          class: Valve
          instance: inlet
          from: Pressurizing
          to: Open
```

---

## Outstanding Questions

1. **Tick semantics** — does `tick: 500ms` advance the clock by exactly 500ms (discrete jump), or does it advance in increments checking for delay queue expiry?
2. **Multiple end states** — can a test declare multiple valid end states, or is it always exactly one?
3. **Trace partial matching** — are all fields in a micro-step assertion required, or are unspecified fields treated as wildcards?

---

*Design session: 2026-03-08 — test file format, execution model, state types, linter rule, mock senescence, and trace assertion syntax defined.*
