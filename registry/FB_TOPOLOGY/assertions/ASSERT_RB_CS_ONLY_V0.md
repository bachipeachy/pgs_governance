# ASSERT_RB_CS_ONLY_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_RB_CS_ONLY_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_RB_CS_ONLY_V0

implementation:
  module: pgs_governance.registry.handlers.assert_rb_cs_only_v0
  callable: execute
```

## Summary

Validates that every binding key in an RB artifact's `core.bindings` map references a CS
artifact (artifact code prefixed with `CS_`). RB artifacts bind CS capabilities to host
implementations — CT, WF, CC, and IN artifact codes are never valid binding targets.

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All RB artifacts

## Handler Behavior

For every RB artifact, for every key in `core.bindings`:
1. The FQDN key MUST resolve to an artifact code starting with `CS_`

## Version History

- **V0**: Initial implementation (2026-05-08)
