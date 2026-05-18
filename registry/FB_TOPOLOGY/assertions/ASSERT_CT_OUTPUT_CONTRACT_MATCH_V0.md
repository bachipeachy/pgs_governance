# ASSERT_CT_OUTPUT_CONTRACT_MATCH_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_CT_OUTPUT_CONTRACT_MATCH_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_CT_OUTPUT_CONTRACT_MATCH_V0

implementation:
  module: pgs_governance.registry.handlers.assert_ct_output_contract_match_v0
  callable: execute
```

## Summary

Validates that CT output keys exactly match CC contract declarations.

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All CT artifacts with `governed_by` binding

## Handler Behavior

For each CT artifact:
1. Load CT Machine section
2. Extract `governed_by` reference to CC
3. Load CC artifact
4. Extract CC `output` declaration keys
5. Load CT implementation code
6. Parse return statements
7. Verify return dict keys match CC output keys exactly
8. Fail if: missing keys, extra keys, or no return statement found

## Error Messages

```
❌ ASSERT_CT_OUTPUT_CONTRACT_MATCH_V0: CT output mismatch
   CT: transforms::CT_EXAMPLE_V0
   CC: governance::CC_EXAMPLE_V0
   Expected keys: ["result", "status"]
   Found keys: ["result"]
   Missing: ["status"]
```
