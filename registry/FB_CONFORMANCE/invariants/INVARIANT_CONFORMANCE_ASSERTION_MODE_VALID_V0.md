# INVARIANT_CONFORMANCE_ASSERTION_MODE_VALID_V0

Architectural Invariant

## Machine

```yaml
invariant_code: INVARIANT_CONFORMANCE_ASSERTION_MODE_VALID_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.conformance::CONSTITUTION_TEST_DATA_V0

core:
  summary: Conformance assertion modes must belong to a closed declared vocabulary
  rule: All assertion specs in TEST_DATA must use declared mode and type values; unknown modes/types are violations
  scope:
    - TEST_DATA
```

## Summary

Every assertion spec in a TEST_DATA artifact must use a `mode` and `type` drawn exclusively from the closed vocabularies declared in this invariant. No implicit, ad-hoc, or undeclared assertion semantics are permitted.

## Rule

For every assertion spec `{field: spec}` in a TEST_DATA `assertions` block:

1. `spec.mode` MUST be present
2. `spec.mode` MUST be in `{ exact, property, schema }`
3. When `mode == property`: `spec.type` MUST be in `{ hex_string, byte_length_range, non_zero }`
4. When `mode == schema`: `spec.type` MUST be `json_schema`
5. Required fields per type MUST be present (see table below)
6. Unknown fields in `spec` beyond declared parameters are violations

## Vocabulary

### Layer 1 — mode (semantic intent)

```
mode ∈ { exact, property, schema }
```

| mode     | Meaning                                                       |
|----------|---------------------------------------------------------------|
| exact    | Field is compared byte-for-byte to expected value (default)  |
| property | Field is validated by structural property (format, size, etc) |
| schema   | Field is validated against a declared JSON schema reference   |

Note: `exact` mode is the default when no `assertions` block is present. An explicit assertion spec with `mode: exact` is valid but redundant — it means use the `expected` dict value for this field.

### Layer 2 — type (validator implementation)

```
property → type ∈ { hex_string, byte_length_range, non_zero }
schema   → type ∈ { json_schema }
```

### Required fields per type

| type              | Required fields         | Optional fields   |
|-------------------|-------------------------|-------------------|
| hex_string        | (none)                  | byte_length       |
| byte_length_range | min, max                | (none)            |
| non_zero          | (none)                  | (none)            |
| json_schema       | schema_ref              | (none)            |

## Enforcement Scope

- **Artifact Types**: TEST_DATA
- **Validation Phase**: VALIDATE_TEST_DATA (compile-time, hard fail)
- **Defense in depth**: conformance runner (runtime, raises AssertionError)
- **Enforcement**: MANDATORY (build fails on violation)

## Examples

### ✅ VALID — property/hex_string with byte_length

```yaml
assertions:
  entropy_bytes:
    mode: property
    type: hex_string
    byte_length: 16
```

### ✅ VALID — property/hex_string without byte_length (format-only check)

```yaml
assertions:
  signature_bytes:
    mode: property
    type: hex_string
```

### ✅ VALID — property/byte_length_range

```yaml
assertions:
  output_bytes:
    mode: property
    type: byte_length_range
    min: 32
    max: 65
```

### ✅ VALID — property/non_zero

```yaml
assertions:
  nonce:
    mode: property
    type: non_zero
```

### ✅ VALID — schema/json_schema

```yaml
assertions:
  response_payload:
    mode: schema
    type: json_schema
    schema_ref: "governance::SCHEMA_ACTOR_RECORD_V0"
```

### ❌ INVALID — missing mode

```yaml
assertions:
  entropy_bytes:
    type: hex_string   # ❌ mode is required
    byte_length: 16
```

### ❌ INVALID — unknown mode

```yaml
assertions:
  entropy_bytes:
    mode: fuzzy        # ❌ not in { exact, property, schema }
    type: hex_string
```

### ❌ INVALID — unknown type for mode

```yaml
assertions:
  entropy_bytes:
    mode: property
    type: random_bytes  # ❌ not in { hex_string, byte_length_range, non_zero }
```

### ❌ INVALID — missing required field

```yaml
assertions:
  output_bytes:
    mode: property
    type: byte_length_range
    min: 32              # ❌ missing max
```

## Rationale

Without a closed assertion vocabulary:
- New assertion types accumulate implicitly in Python runner code
- Test semantics become opaque — the assertion contract is not declared anywhere
- Compiler cannot validate test data shape at build time
- Conformance results lose their proof value ("70/70 PASS" means something only if the assertion model is formally bounded)

This invariant ensures that the conformance suite's claim of correctness is enforced by construction, not convention.

## Related Artifacts

- `fb.conformance::CONSTITUTION_TEST_DATA_V0` - Governs TEST_DATA structure
- `governance::INVARIANT_TEST_DATA_MATCH_CT_OUTPUT_V0` - Complementary: output keys must match CT contract
- `governance::INVARIANT_CT_OUTPUT_CONTRACT_MATCH_V0` - CT output purity
