# ASSERT_ATOM_OUTPUT_PURITY_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_ATOM_OUTPUT_PURITY_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_ATOM_OUTPUT_PURITY_V0

implementation:
  module: pgs_governance.registry.handlers.assert_atom_output_purity_v0
  callable: execute
```

## Summary

Validates that CT atom implementations return explicit outputs in all code paths, never raise exceptions for business logic.

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All CT atom implementation files

## Handler Behavior

For each CT atom Python file:
1. Parse AST
2. Find `execute()` function definition
3. Scan function body for:
   - `raise` statements after input validation block
   - Conditional branches without return statements
   - Business logic exceptions (not ValueError/TypeError for inputs)
4. Verify all code paths return dict

## Error Messages

```
❌ ASSERT_ATOM_OUTPUT_PURITY_V0: Business logic exception detected
   File: pgs_transforms/implementation/transforms/atoms/ct_pure_check_quota_v0.py
   Function: execute
   Line 42: raise ValueError("Quota exhausted")
   Violation: Exception raised for business logic (not input validation)
   Fix: Return explicit output dict {"quota_available": False} instead
```
