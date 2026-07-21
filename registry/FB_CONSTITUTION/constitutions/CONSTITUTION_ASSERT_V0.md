# CONSTITUTION_ASSERT_V0

## Machine
```yaml
fqdn: fb.constitution::CONSTITUTION_ASSERT_V0
constitution_code: CONSTITUTION_ASSERT_V0
artifact_kind: CONSTITUTION
version: V0
governed_by: fb.vocabulary::CONSTITUTION_VOCABULARY_V0

core:
  description: >
    Governs ASSERT — the compiler-derived executable projection of an INVARIANT.
    ASSERT is NOT a hand-authored artifact: the compiler synthesizes ASSERT_X from
    INVARIANT_X at governance time (S4), binding a handler by convention
    (handlers.assert_<stem>) or an invariant `assert_projection.handler` override,
    and drawing check parameters from the invariant's `assert_projection`. Covers
    binding, purity, compiler-only execution, and violations output.
  scope: artifact
  governs:
    - ASSERT
  derivation:
    authored: false
    derived_from: INVARIANT
    rule: "ASSERT_X is the executable projection of INVARIANT_X; parameters come from the invariant's assert_projection block"
  enforcement_model: compiler_enforced

rules:
  - rule_id: ASSERT_BINDS_ONE_INVARIANT
    applies_to: ASSERT
    constraint: every ASSERT MUST enforce exactly one INVARIANT
    enforced_by: TBD

  - rule_id: ASSERT_COMPILER_ONLY
    applies_to: ASSERT
    constraint: ASSERT MUST execute during compiler ASSERT phase only; never at runtime
    enforced_by: TBD

  - rule_id: ASSERT_PURITY
    applies_to: ASSERT
    constraint: ASSERT MUST be pure, deterministic, and side-effect free
    enforced_by: TBD

  - rule_id: ASSERT_VIOLATIONS_OUTPUT
    applies_to: ASSERT
    constraint: ASSERT MUST return violations array; missing output is a constitutional violation
    enforced_by: TBD
```

---

## 1. Purpose

Defines the canonical structure and semantics of **ASSERT artifacts**.

An ASSERT evaluates an INVARIANT and produces violations.

ASSERT execution occurs during compiler validation.

---

## 2. Core Model

```text
INVARIANT → declares constraint
ASSERT    → evaluates constraint
COMPILER  → enforces constraint
```

## 3. Core Principles

### 3.1 Mandatory Binding

Every ASSERT MUST enforce exactly one INVARIANT.

### 3.2 Compiler Execution Only

ASSERT MUST execute in compiler validation phase.

ASSERT MUST NOT execute in:
- CT pipeline
- CS pipeline
- workflow runtime

### 3.3 Purity

ASSERT MUST be:
- pure
- deterministic
- side-effect free

### 3.4 Fail-Fast

Any violation MUST cause compilation failure.
No warnings. No partial success.

### 3.5 Explicit Output

ASSERT MUST return violations array.

## 4. Required Fields (Documentation)

```yaml
assert_code: ASSERT_<NAME>_V<N>
artifact_kind: ASSERT
version: V<N>
governed_by: fb.constitution::CONSTITUTION_ASSERT_V0

enforces: INVARIANT_<NAME>_V<N>

core:
  summary: <one-line>
  description: <detailed description>

inputs: {}

outputs:
  violations:
    type: ARRAY
    element_type: ConformanceViolation
    required: true

logic:
  description: <evaluation logic>

purity:
  pure: true
  side_effects: NONE
  deterministic: true
```

## 5. Output Contract (Documentation)

```yaml
violations:
  - artifact_fqdn: <string>
    violation_code: <string>
    message: <string>
    severity: CRITICAL
```

## 6. Binding Contract

### 6.1 Required

ASSERT.enforces MUST reference exactly one INVARIANT.

### 6.2 Consistency Rule

ASSERT.enforces MUST match INVARIANT.enforced_by.

### 6.3 Illegal States

System MUST fail if:
- ASSERT has no INVARIANT
- ASSERT references missing INVARIANT
- mismatch exists

## 7. Execution Model

Compiler MUST execute:
Discovery
→ Parse
→ Validation
→ ASSERT
→ Materialization

## 8. Enforcement Semantics

```python
for assert in ASSERTS:
    result = evaluate(assert)
    if result.violations:
        FAIL_BUILD(result.violations)
```

## 9. Forbidden Behavior

- ASSERT in CT pipeline
- ASSERT in runtime
- ASSERT with side effects
- ASSERT without violations output

## 10. Naming

`ASSERT_<CONSTRAINT>_V<N>`

## 11. System Guarantees

No violation survives compilation.

## 12. Constitutional Violations

- missing enforces
- impurity
- missing violations output
- runtime execution

## 13. One-Line Truth

ASSERT makes invariants enforceable.
