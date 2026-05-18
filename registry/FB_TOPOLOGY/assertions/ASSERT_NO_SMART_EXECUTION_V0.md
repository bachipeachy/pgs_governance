# ASSERT_NO_SMART_EXECUTION_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_NO_SMART_EXECUTION_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_NO_SMART_EXECUTION_V0

implementation:
  module: pgs_governance.registry.handlers.assert_no_smart_execution_v0
  callable: execute
```

## Summary

Validates that execution layer code does not perform type-based conversions or interpretations.

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: pgs_execution code (atom_registry, workflow_runner, etc.)

## Handler Behavior

Scans execution layer Python files for:
1. Type metadata loading calls (`load_contract`, `_load_atom_output_types`)
2. Type-based conditionals (`if type == "hex_string"`)
3. Type conversion calls (`.hex()`, `bytes.fromhex()`)
4. Type caching (`_OUTPUT_TYPES_CACHE`)

Fails if any pattern detected.

## Error Messages

```
❌ ASSERT_NO_SMART_EXECUTION_V0: Smart executor detected
   File: pgs_execution/execution/machine/transforms/atom_registry.py
   Line 257: if step_input_types.get(key) == "hex_string":
   Violation: Type-based conditional (smart execution)
   Fix: Remove type interpretation, move canonicalization to atoms
```
