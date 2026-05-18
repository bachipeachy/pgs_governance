# ASSERT_IN_NO_EXECUTION_LOGIC_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_IN_NO_EXECUTION_LOGIC_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_IN_NO_EXECUTION_LOGIC_V0

implementation:
  module: pgs_governance.registry.handlers.assert_in_no_execution_logic_v0
  callable: execute
```

## Summary

Validates that IN (Intent) artifacts do not contain execution logic fields. Intents are
admission gates — they declare what is required for entry, not how to process the payload.
Execution belongs in CC and CT artifacts.

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All IN artifacts

## Handler Behavior

For every IN artifact, the frontmatter MUST NOT contain any of the following reserved
execution fields at any level:
- `execute`
- `callable`
- `implementation`
- `logic`
- `transform`
- `code`
- `handler`

## Version History

- **V0**: Initial implementation (2026-05-08)
