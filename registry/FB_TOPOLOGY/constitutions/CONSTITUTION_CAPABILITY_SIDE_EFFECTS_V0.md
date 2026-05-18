# CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0

## Machine
```yaml
fqdn: fb.topology::CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0
constitution_code: CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0
artifact_kind: CONSTITUTION
version: V0
governed_by: fb.vocabulary::CONSTITUTION_VOCABULARY_V0

core:
  description: Governs Capability Side Effect (CS) artifacts — explicit declaration, traceability, and isolation
  scope: artifact
  governs:
    - CS
  enforcement_model: compiler_enforced

rules:
  - rule_id: CS_EXPLICIT_DECLARATION
    applies_to: CS
    constraint: all side effects MUST be explicitly declared in protocol; no implicit side effects
    enforced_by: ASSERT_CS_SURFACE_CLOSED_V0

  - rule_id: CS_IMPLEMENTATION_DECLARED
    applies_to: CS
    constraint: CS MUST declare implementation with non-empty module and callable
    enforced_by: ASSERT_CS_SURFACE_CLOSED_V0

  - rule_id: CS_TRACEABLE
    applies_to: CS
    constraint: every CS execution MUST be recorded in the execution trace
    enforced_by: ASSERT_CS_TRACEABLE_V0

  - rule_id: CS_ISOLATED_EXECUTION
    applies_to: CS
    constraint: CS MUST execute through dedicated executors only; not inline in CT or CC
    enforced_by: ASSERT_CS_ISOLATED_EXECUTION_V0
```

---

## 1. Purpose

This constitution defines the governance and enforcement rules for Capability Side Effects (CS).

Capability Side Effects are the mechanism for interacting with the outside world, such as databases, external APIs, and filesystem.

---

## 2. Core Principles

- **Explicit Declaration:** All side effects must be explicitly declared in the protocol.
- **Isolated Execution:** Side effects must be executed through dedicated executors.
- **Traceability:** Every execution of a side effect must be recorded in the trace.
- **Limited Mutability:** Side effects should be restricted to the necessary scope of mutability.

---

## 3. Required Fields

- `cs_code`: Unique identifier for the side effect.
- `version`: Version of the side effect.
- `governed_by`: The constitution governing this side effect.
- `core`: Metadata and description.
- `inputs`: Definition of input parameters.
- `outputs`: Definition of output parameters (e.g., success status, return data).
- `logic`: Reference to the implementation executor.

---

## 4. Validation Rules

- Side effect implementations must be discoverable.
- Input and output types must match the capability contract.
- Side effects must be restricted to authorized layers.
