# ASSERT_EXECUTION_PLACEMENT_DECLARED_V0

## Machine

```yaml
artifact_code: ASSERT_EXECUTION_PLACEMENT_DECLARED_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.execution_placement::INVARIANT_EXECUTION_PLACEMENT_DECLARED_V0

implementation:
  module: pgs_governance.registry.handlers.assert_execution_placement_declared_v0
  callable: execute

enforcement:
  phase: assert
  failure_mode: HARD_FAIL
  scope: ALL_ARTIFACTS
```

---

## Summary

Validates that exactly one active placement contract exists in `FB_EXECUTION_PLACEMENT`.

Enforces `INVARIANT_EXECUTION_PLACEMENT_DECLARED_V0`: every compiled snapshot must
declare active execution placement semantics. Zero contracts is a missing declaration.
More than one active contract is an ambiguity violation.

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL
- **Scope**: All artifacts (scans `fb.execution_placement` namespace)
