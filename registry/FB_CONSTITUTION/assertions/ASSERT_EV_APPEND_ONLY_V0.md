# ASSERT_EV_APPEND_ONLY_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_EV_APPEND_ONLY_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.constitution::INVARIANT_EV_APPEND_ONLY_V0

implementation:
  module: pgs_governance.registry.handlers.assert_ev_append_only_v0
  callable: execute
```

## Summary

Validates that EV artifacts do not declare mutation operations. Events are append-only;
an EV artifact MUST NOT declare `update`, `delete`, `patch`, or `mutate` fields in its
schema or extensions block.

The runtime enforcement (actual store append-only semantics) is handled by CS_APPENDONLY_JSONL_V0.
This ASSERT provides compile-time verification that the artifact declaration is conformant.

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All EV artifacts

## Handler Behavior

For every EV artifact:
1. `core.schema` MUST NOT contain fields named `_update`, `_delete`, `_patch`, `_mutate`
2. `extensions` MUST NOT declare mutation operation keys

## Version History

- **V0**: Initial implementation (2026-05-08)
