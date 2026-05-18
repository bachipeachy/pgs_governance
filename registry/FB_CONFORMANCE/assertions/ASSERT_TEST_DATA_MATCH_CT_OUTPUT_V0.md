# ASSERT_TEST_DATA_MATCH_CT_OUTPUT_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_TEST_DATA_MATCH_CT_OUTPUT_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.conformance::INVARIANT_TEST_DATA_MATCH_CT_OUTPUT_V0

implementation:
  module: pgs_governance.registry.handlers.assert_test_data_match_ct_output_v0
  callable: execute
```

## Summary

Validates that TEST_DATA expected outputs match target CT output contract.

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All TEST_DATA artifacts

## Handler Behavior

For each TEST_DATA artifact:
1. Load TEST_DATA Machine section
2. Extract test_target CT reference
3. Load target CT artifact
4. Extract CT's governed_by CC reference
5. Load CC artifact
6. Extract CC output declaration keys
7. For each test case in TEST_DATA:
   - Verify `expected` keys match CC output keys exactly
   - Fail if: missing keys or extra keys

## Error Messages

```
❌ ASSERT_TEST_DATA_MATCH_CT_OUTPUT_V0: TEST_DATA expected mismatch
   TEST_DATA: transforms::TEST_DATA_HASH_V0
   CT: transforms::CT_HASH_DATA_V0
   CC: governance::CC_HASH_DATA_V0
   Expected keys: ["hash_value"]
   Test case 1 has keys: ["hash_value", "extra_field"]
   Extra keys: ["extra_field"]
```
