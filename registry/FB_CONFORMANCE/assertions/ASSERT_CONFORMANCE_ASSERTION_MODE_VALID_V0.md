# ASSERT_CONFORMANCE_ASSERTION_MODE_VALID_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_CONFORMANCE_ASSERTION_MODE_VALID_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.conformance::INVARIANT_CONFORMANCE_ASSERTION_MODE_VALID_V0

implementation:
  module: pgs_governance.registry.handlers.assert_conformance_assertion_mode_valid_v0
  callable: execute
```

## Summary

Registers the INVARIANT_CONFORMANCE_ASSERTION_MODE_VALID_V0 invariant in the assertion parity surface.

The actual closed-vocabulary enforcement (mode ∈ {exact, property, schema}, type constraints) is performed
by the VALIDATE_TEST_DATA compiler phase. This ASSERT exists to maintain 1:1 parity between INVARIANT
and ASSERT artifacts and to make the invariant visible in the compiler assertion surface.

## Enforcement

- **Phase**: 5 (ASSERT) — parity registration only
- **Primary Enforcement**: Phase 7 (VALIDATE_TEST_DATA) — hard fail on unknown modes/types
- **Failure Mode**: PASSED (enforcement delegated to VALIDATE_TEST_DATA phase)
- **Scope**: All TEST_DATA artifacts

## Version History

- **V0**: Initial implementation (2026-05-08)