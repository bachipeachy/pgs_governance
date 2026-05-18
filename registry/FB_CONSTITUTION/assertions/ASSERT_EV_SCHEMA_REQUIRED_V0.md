# ASSERT_EV_SCHEMA_REQUIRED_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_EV_SCHEMA_REQUIRED_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.constitution::INVARIANT_EV_SCHEMA_REQUIRED_V0

implementation:
  module: pgs_governance.registry.handlers.assert_ev_schema_required_v0
  callable: execute
```

## Summary

Validates that every EV (Event) artifact declares a non-empty `core.schema` block.
A schema-less event cannot specify what data it carries, violating auditability and
replay guarantees.

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All EV artifacts

## Handler Behavior

For every EV artifact:
1. `core.schema` MUST be present
2. `core.schema` MUST be a non-empty mapping (at least one field declared)

## Version History

- **V0**: Initial implementation (2026-05-08)
