# ASSERT_CC_STORAGE_OP_CONFORMANCE_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_CC_STORAGE_OP_CONFORMANCE_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_CC_STORAGE_OP_CONFORMANCE_V0

enforcement:
  order: 42
  level: ERROR

implementation:
  module: pgs_governance.registry.handlers.assert_cc_storage_op_conformance_v0
  callable: execute
```

## Summary

Validates that every CC pipeline step with a `side_effect` binding declares an `op`
that exists in the target CS's `core.policy.operations` list.

## Enforcement

- **Phase**: S4_GOVERN (governance validation)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All CC artifacts with CS-binding pipeline steps

## Handler Behavior

### 1. Read pre-computed op conformance analysis

The compiler pre-computes `cc_op_conformance` in `_precompute_structural_analysis`.
This handler reads that pre-computed result and surfaces violations.

### 2. Validate each CC

For each CC with CS-binding pipeline steps:
- Check that the `op` value is in the target CS's declared operations
- Surface violations for any step where op ∉ CS.core.policy.operations

### 3. Aggregate violations

Collect violations across all CC artifacts. Return result with violation details.

## Error Messages

### Undeclared Op
```
❌ ASSERT_CC_STORAGE_OP_CONFORMANCE_V0: Operation not declared by target CS
   CC: CC_CHECK_VALIDATOR_EXISTS_V0
   Step: check_validator_exists
   Op declared: GET
   CS: capability_side_effects::CS_MUTABLE_JSON_V0
   CS declared ops: [READ, WRITE, DELETE, EXISTS, LIST]
   Fix: Change op to one of the declared operations
```

## Rationale

Moves op-name mismatch detection from runtime BACKEND_ERROR to compile-time failure.
Enforces the protocol-first principle: CS declares its vocabulary; CC must conform;
compiler verifies; runtime executes verbatim.

## Version History

- **V0**: Initial implementation (2026-05-29) — CC storage operation conformance assertion
