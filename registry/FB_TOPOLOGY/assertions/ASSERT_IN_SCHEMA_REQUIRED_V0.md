# ASSERT_IN_SCHEMA_REQUIRED_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_IN_SCHEMA_REQUIRED_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_IN_SCHEMA_REQUIRED_V0

implementation:
  module: pgs_governance.registry.handlers.assert_in_schema_required_v0
  callable: execute
```

## Summary

Validates that every IN artifact declares a non-empty inputs block:
1. IN artifact must have a core.inputs field (not a top-level schema field)
2. core.inputs must declare at least one field
3. Each declared input field must have a non-empty type

## Enforcement

- **Phase**: 4 (VALIDATE)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All IN artifacts

## Handler Behavior

### 1. Check Inputs Presence

Verify each IN artifact has core.inputs.

Violation: core.inputs missing or null.

### 2. Check Inputs Non-Empty

Verify core.inputs declares at least one field.

Violation: core.inputs is an empty mapping.

### 3. Check Field Types

Verify each input field declares a non-empty type.

Violation: field present but type missing or empty.

## Error Messages

### Missing Schema
```
❌ ASSERT_IN_SCHEMA_REQUIRED_V0: Missing schema
   IN: IN_EXAMPLE_V0
   Violation: IN artifact must declare a schema
   Fix: Add schema field with at least one typed field declaration
```

### Empty Schema
```
❌ ASSERT_IN_SCHEMA_REQUIRED_V0: Empty schema
   IN: IN_EXAMPLE_V0
   Violation: IN schema must declare at least one field
   Fix: Declare at least one input field in schema
```

## Rationale

Intent artifacts are admission gates. A schema-less intent cannot validate
incoming payloads, defeating the purpose of the admission check. Every intent
must declare what it expects.

## Version History

- **V0**: Initial implementation (2026-05-04)
