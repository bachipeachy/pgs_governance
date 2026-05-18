# INVARIANT_CS_ISOLATED_EXECUTION_V0

Architectural Invariant

## Machine

```yaml
invariant_code: INVARIANT_CS_ISOLATED_EXECUTION_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.topology::CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0

core:
  summary: CS must execute through dedicated executors only; not inline in CT or CC
  rule: CS artifacts must not be called directly from CT transform logic or CC wiring
  scope:
    - CS
```

## Summary

Capability Side Effects must be invoked exclusively through the runtime's dedicated
executor mechanism. CS cannot be called inline from within a CT (Capability Transform)
or embedded as direct execution logic in a CC (Capability Contract). This separation
is what makes side effects declarative, governable, and traceable.

## Rule

1. CT artifacts MUST NOT directly invoke CS implementations — all CS access goes through the CC execution layer
2. CC artifacts MUST reference CS via declared binding keys — never via direct module import or inline execution

This invariant is enforced at runtime by the execution engine's executor routing.

## Enforcement Scope

- **Artifact Types**: CS
- **Validation Phase**: Runtime (executor routing)
- **Compile-Time**: ASSERT_CS_ISOLATED_EXECUTION_V0 (parity stub — runtime enforcement)
- **Enforced By**: ASSERT_CS_ISOLATED_EXECUTION_V0

## Rationale

Inline CS execution in CT or CC logic bypasses the executor mechanism, breaks traceability,
circumvents runtime binding, and creates implicit coupling between declared artifacts and
implementation details. Isolated execution through the executor is the only way to guarantee
that CS behavior matches its declared contract.
