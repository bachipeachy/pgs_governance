# INVARIANT_CT_OUTPUT_CONTRACT_MATCH_V0

Architectural Invariant

## Machine

```yaml
invariant_code: INVARIANT_CT_OUTPUT_CONTRACT_MATCH_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0

core:
  summary: CT output structure must match declared capability contract
  rule: All CT artifacts must produce outputs matching their CC declaration keys and types
  scope:
    - CT
```

## Summary

Every Capability Transform (CT) must produce outputs that exactly match the keys declared in its governing Capability Contract (CC).

## Rule

For every CT artifact:
1. CT must declare `governed_by` binding to a CC artifact
2. CC must declare `output` section with explicit keys
3. CT implementation must return dict with EXACTLY those keys
4. Extra keys, missing keys, or mismatched types are violations

## Enforcement Scope

- **Artifact Types**: CT
- **Validation Phase**: Phase 5 (ASSERT)
- **Enforcement**: MANDATORY (build fails on violation)

## Examples

### ✅ VALID

**CC Declaration:**
```yaml
output:
  seed_bytes: hex_string
```

**CT Implementation:**
```python
def execute(inputs, context=None):
    return {
        "seed_bytes": "0x123abc..."
    }
```

### ❌ INVALID

**Missing key:**
```python
return {}  # ❌ Missing "seed_bytes"
```

**Extra key:**
```python
return {
    "seed_bytes": "0x123abc...",
    "extra_field": "value"  # ❌ Not in contract
}
```

## Rationale

Output contract matching ensures:
- Predictable transform behavior
- Type safety at compilation
- Explicit interface contracts
- No hidden outputs
- Traceable data flow

## Related Artifacts

- `fb.topology::CONSTITUTION_CAPABILITY_TRANSFORMS_V0` - Governs CT behavior
- `fb.topology::CONSTITUTION_CAPABILITY_CONTRACT_V0` - Defines CC schema
