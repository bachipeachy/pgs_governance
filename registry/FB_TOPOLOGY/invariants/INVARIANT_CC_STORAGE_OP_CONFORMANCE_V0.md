# INVARIANT_CC_STORAGE_OP_CONFORMANCE_V0

## Machine

```yaml
invariant_code: INVARIANT_CC_STORAGE_OP_CONFORMANCE_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  description: >
    Each CC pipeline step that binds a CS (side_effect) must declare an `op`
    that is a member of that CS's `core.policy.operations` list.

    The CS artifact is the authoritative declaration of its supported operation
    vocabulary. A CC may not invoke an operation the CS does not declare.
    Unknown ops produce runtime BACKEND_ERROR — this invariant moves that
    failure to compile time.

  enforcement_stage:
    - compiler_validation

  scope:
    - CAPABILITY_CONTRACTS

  violation_response: FAIL_IMMEDIATELY


  anti_patterns:
    - undeclared_op: "CC pipeline step declares op not in CS.core.policy.operations"
    - missing_op: "CC pipeline step with side_effect binding has no op declared"

  clarification:
    single_vocabulary: >
      The canonical operation vocabulary for each CS is declared in
      CS.core.policy.operations. This is the protocol-layer source of truth.
      CC authors must use ops from that list. The compiler enforces this;
      the runtime never aliases or translates op names.
    ct_steps_exempt: >
      Pipeline steps that bind a CT (transform) are exempt — transforms have
      no op field. Only CS-binding steps are subject to this invariant.

# assert_projection — parameters the compiler-derived ASSERT carries (ASSERT is derived, not authored)
assert_projection:
  enforcement:
    order: 42
    level: ERROR
```

---

## Purpose

Ensure CC pipeline steps invoke only operations that the target CS explicitly declares.

**Core Principle**: Operation vocabulary is declared in protocol, enforced by compiler, executed verbatim by runtime. No translation, no aliasing, no heuristics.

---

## Validation Rules

### Rule 1: op ∈ CS.core.policy.operations

For every CC pipeline step with a `side_effect` binding:
- The step must declare an `op` field
- The declared `op` must exist in the target CS's `core.policy.operations` list

**Violation — Undeclared Op**:
```yaml
# ❌ FORBIDDEN — CS_MUTABLE_JSON_V0 declares READ not GET
pipeline:
  - step: check_exists
    side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
    op: GET   # ❌ GET is not in CS_MUTABLE_JSON_V0.core.policy.operations
```

**Correct**:
```yaml
# ✅ op matches CS declaration
pipeline:
  - step: check_exists
    side_effect: capability_side_effects::CS_MUTABLE_JSON_V0
    op: READ  # ✓ READ is declared in CS_MUTABLE_JSON_V0.core.policy.operations
```

---

## Rationale

Without this invariant, a CC can declare any string as `op`. The compiler accepts
it. The runtime dispatches via `getattr(engine, op.lower(), None)`. If no handler
method matches, the result is BACKEND_ERROR at execution time — a runtime failure
that was detectable at compile time.

This invariant closes the gap: **Governance declares → Compiler enforces → Runtime executes.**

---

## Version History

- **V0**: Initial implementation (2026-05-29) — CC operation conformance enforcement
