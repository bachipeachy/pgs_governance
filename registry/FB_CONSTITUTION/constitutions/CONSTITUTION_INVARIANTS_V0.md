# CONSTITUTION_INVARIANTS_V0

## Machine
```yaml
fqdn: fb.constitution::CONSTITUTION_INVARIANTS_V0
constitution_code: CONSTITUTION_INVARIANTS_V0
artifact_kind: CONSTITUTION
version: V0
governed_by: fb.vocabulary::CONSTITUTION_VOCABULARY_V0

core:
  description: Governs INVARIANT artifacts — declarative constraints that must never be violated
  scope: artifact
  governs:
    - INVARIANT
  enforcement_model: compiler_enforced

rules:
  - rule_id: INVARIANT_DECLARATIVE_ONLY
    applies_to: INVARIANT
    constraint: INVARIANT MUST declare constraints only; MUST NOT contain executable logic
    enforced_by: TBD

  - rule_id: INVARIANT_MANDATORY_ENFORCEMENT
    applies_to: INVARIANT
    constraint: every INVARIANT MUST be enforced by at least one ASSERT
    enforced_by: TBD

  - rule_id: INVARIANT_FAIL_FAST
    applies_to: INVARIANT
    constraint: violation_response MUST be FAIL_IMMEDIATELY; no warnings, no partial success
    enforced_by: TBD
```

---

## 1. Purpose

Defines the canonical structure and semantics of **INVARIANT artifacts**.

An INVARIANT declares a **cross-cutting constraint that MUST always hold true**.

INVARIANTS are declarative and are enforced via ASSERT artifacts during compilation.

---

## 2. Core Model

```text
INVARIANT → declares constraint
ASSERT    → evaluates constraint
COMPILER  → enforces constraint
```

## 3. Core Principles

### 3.1 Declarative Only

INVARIANTS MUST declare constraints only.
They MUST NOT contain executable logic.

### 3.2 Mandatory Enforcement

Every INVARIANT MUST be enforced by at least one ASSERT.

### 3.3 Fail-Fast

Violations MUST result in immediate compilation failure.

### 3.4 Negative Enforcement

INVARIANTS define forbidden states:
- System MUST NOT do X

### 3.5 No Conditional Enforcement

INVARIANTS are always enforced.
No debug modes, no environment toggles.

## 4. Required Fields (Documentation)

```yaml
invariant_code: INVARIANT_<NAME>_V<N>
artifact_kind: INVARIANT
version: V<N>
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: <constraint description>

  enforcement_stage:
    - compiler_validation

  scope:
    - <artifact_types>

  violation_response: FAIL_IMMEDIATELY

  enforced_by:
    - ASSERT_<NAME>_V<N>

  anti_patterns:
    - <pattern>: "<description>"

  clarification:
    <case>: "<boundary explanation>"
```

## 5. Binding Contract

### 5.1 Required

Every INVARIANT MUST:
- declare enforced_by ASSERT(s)

### 5.2 Consistency Rule

INVARIANT.enforced_by MUST match ASSERT.enforces

### 5.3 Illegal States

System MUST fail if:
- INVARIANT has no ASSERT
- ASSERT does not reference INVARIANT
- mismatch exists

## 6. Enforcement Semantics

- INVARIANT does NOT execute
- ASSERT evaluates INVARIANT
- COMPILER enforces result

## 7. Naming

`INVARIANT_<CONSTRAINT>_V<N>`

## 8. System Guarantees

No constraint exists without enforcement

## 9. Constitutional Violations

- Missing enforced_by
- violation_response not FAIL_IMMEDIATELY
- missing enforcement_stage
- missing anti_patterns

## 10. One-Line Truth

INVARIANT defines what must never be violated.
