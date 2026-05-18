# CONSTITUTION_CAPABILITY_TRANSFORMS_V0

## Machine
```yaml
fqdn: fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0
constitution_code: CONSTITUTION_CAPABILITY_TRANSFORMS_V0
artifact_kind: CONSTITUTION
version: V0
governed_by: fb.vocabulary::CONSTITUTION_VOCABULARY_V0

core:
  description: Governs Capability Transform (CT) artifacts — purity, determinism, and explicit IO
  scope: artifact
  governs:
    - CT
  enforcement_model: compiler_enforced

rules:
  - rule_id: CT_PURITY
    applies_to: CT
    constraint: CT MUST be a pure function; same inputs MUST always produce same outputs
    enforced_by: TBD

  - rule_id: CT_NO_SIDE_EFFECTS
    applies_to: CT
    constraint: CT MUST NOT produce side effects; side effects belong in CS
    enforced_by: TBD

  - rule_id: CT_IMPLEMENTATION_DECLARED
    applies_to: CT
    constraint: atom CT MUST declare machine.implementation with non-empty module and callable
    enforced_by: ASSERT_CT_SURFACE_CLOSED_V0

  - rule_id: CT_EXPLICIT_IO
    applies_to: CT
    constraint: all CT inputs and outputs MUST be explicitly declared
    enforced_by: TBD
```

---

## 1. Purpose

This constitution defines the governance and enforcement rules for Capability Transforms (CT).

Capability Transforms are pure functions that transform data within the protocol. They are the primary mechanism for logic in the system.

---

## 2. Core Principles

- **Purity:** All CTs MUST be pure functions.
- **Determinism:** Given the same input, a CT MUST always produce the same output.
- **Side-Effect Free:** CTs MUST NOT have side effects. Side effects are delegated to Capability Side Effects (CS).
- **Explicit Inputs/Outputs:** All data required by a CT must be passed as explicit inputs. All results must be returned as explicit outputs.

---

## 3. Required Fields

- `ct_code`: Unique identifier for the transform.
- `version`: Version of the transform.
- `governed_by`: The constitution governing this transform.
- `core`: Metadata and description.
- `inputs`: Definition of input parameters.
- `outputs`: Definition of output parameters.
- `logic`: Reference to the implementation.

---

## 4. Validation Rules

- CT implementations must be discoverable.
- Input and output types must match the capability contract.
- Implementation must adhere to the purity principle.
