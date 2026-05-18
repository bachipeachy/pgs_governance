# INVARIANT_TEST_DATA_MATCH_CT_OUTPUT_V0

Architectural Invariant

## Machine

```yaml
invariant_code: INVARIANT_TEST_DATA_MATCH_CT_OUTPUT_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  summary: TEST_DATA expected outputs must match CT output contract
  rule: All TEST_DATA artifacts must declare expected outputs matching their target CT output keys
  scope:
    - TEST_DATA
```

## Summary

Every TEST_DATA artifact must declare `expected` outputs with keys that exactly match the output contract of its target CT.

## Rule

For every TEST_DATA artifact:
1. TEST_DATA must reference a target CT (via test_target or equivalent)
2. TEST_DATA must declare `expected` section
3. Expected keys must match CT's CC output declaration
4. Missing keys or extra keys are violations

## Enforcement Scope

- **Artifact Types**: TEST_DATA
- **Validation Phase**: Phase 5 (ASSERT)
- **Enforcement**: MANDATORY (build fails on violation)

## Examples

### ✅ VALID

**CT Output Contract (from CC):**
```yaml
output:
  seed_bytes: hex_string
  is_valid: bool
```

**TEST_DATA:**
```yaml
test_cases:
  - inputs: {...}
    expected:
      seed_bytes: "NOT_NONE"
      is_valid: true
```

### ❌ INVALID

**Missing key:**
```yaml
expected:
  seed_bytes: "NOT_NONE"
  # ❌ Missing "is_valid"
```

**Extra key:**
```yaml
expected:
  seed_bytes: "NOT_NONE"
  is_valid: true
  bonus_field: "value"  # ❌ Not in CT contract
```

## Rationale

TEST_DATA contract matching ensures:
- Test coverage completeness
- Catch contract changes at compile time
- No silent test gaps
- Explicit test expectations
- Traceable conformance validation

## Related Artifacts

- `governance::INVARIANT_CT_OUTPUT_CONTRACT_MATCH_V0` - Complementary check
- `fb.conformance::CONSTITUTION_TEST_DATA_V0` - Governs TEST_DATA structure
