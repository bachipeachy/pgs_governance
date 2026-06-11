# ASSERT_CT_TEST_DATA_OUTCOME_DECLARED_V0

Governance Assertion

## Machine

```yaml
artifact_code: ASSERT_CT_TEST_DATA_OUTCOME_DECLARED_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_CT_TEST_DATA_OUTCOME_DECLARED_V0

implementation:
  module: pgs_governance.registry.handlers.assert_ct_test_data_outcome_declared_v0
  callable: execute
```

## Summary

Every test case in a TEST_DATA artifact must declare an explicit `expected_outcome`.
This assertion validates that all case yaml blocks in all TEST_DATA artifacts carry
the field — preventing the compiler from defaulting absent values to SUCCESS and
silently masking VIOLATION test cases.

## Rule

For every TEST_DATA artifact in the compiled graph:
1. Parse all `### Case N: case_id` yaml blocks from the artifact content.
2. Each yaml block must contain `expected_outcome` as an explicit key.
3. The value must be one of: `SUCCESS`, `VIOLATION`.
4. A case yaml block without `expected_outcome` is a compile-time violation.

## Enforcement

- **Artifact Types**: TEST_DATA
- **Validation Phase**: compile_time (S4 GOVERN)
- **Handler**: `pgs_governance.registry.handlers.assert_ct_test_data_outcome_declared_v0`
- **Paired Invariant**: INVARIANT_CT_TEST_DATA_OUTCOME_DECLARED_V0

## Rationale

The conformance test runner uses `expected_outcome` to determine whether a CT
invocation should succeed or raise a VIOLATION. A missing field forces the runner
to either default silently (hiding VIOLATION test failures) or fail cryptically.

This assertion catches the omission at compile time — before any test artifact is
generated — so the test author receives a named governance error they can trace
back to a specific case in a specific TEST_DATA file.
