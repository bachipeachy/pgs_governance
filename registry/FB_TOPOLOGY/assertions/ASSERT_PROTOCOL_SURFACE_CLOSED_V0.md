# ASSERT_PROTOCOL_SURFACE_CLOSED_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_PROTOCOL_SURFACE_CLOSED_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_PROTOCOL_SURFACE_CLOSED_V0

implementation:
  module: pgs_governance.registry.handlers.assert_protocol_surface_closed_v0
  callable: execute
```

## Summary

Validates all FQDN references resolve to existing artifacts.

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All compiled artifacts

## Old Content (preserved for reference)

outputs:
  violations:
    type: ARRAY
    element_type: ConformanceViolation
    required: true
    schema:
      - artifact_fqdn: STRING (artifact with violation)
      - violation_code: STRING (DANGLING_REFERENCE | SHORT_NAME_REFERENCE)
      - message: STRING (human-readable description)
      - severity: STRING (CRITICAL)

logic:
  description: |
    FOR EACH artifact IN artifacts_by_fqdn:
      references = extract_references(artifact)  # canonical + fallback

      FOR EACH reference IN references:
        # Check 1: Dangling reference
        IF reference NOT IN artifacts_by_fqdn:
          APPEND violation:
            code: DANGLING_REFERENCE
            message: "Reference {reference} not found in compilation graph"

        # Check 2: Short name reference
        IF "::" NOT IN reference:
          APPEND violation:
            code: SHORT_NAME_REFERENCE
            message: "Reference {reference} not FQDN-normalized"

    IF violations NOT EMPTY:
      RETURN violations
    ELSE:
      RETURN []

purity:
  pure: true
  side_effects: NONE
  deterministic: true
  idempotent: true
```

---

## Purpose

Enforce INVARIANT_PROTOCOL_SURFACE_CLOSED_V0 during compilation.

**Execution Phase**: ASSERT (after VALIDATE, before MATERIALIZE)

**Failure Mode**: Build fails immediately on any violation (no warnings).

---

## Implementation Notes

### Reference Extraction

Uses `_extract_references()` utility to handle multiple reference patterns:

```python
def _extract_references(artifact: dict) -> list[str]:
    """
    Extract references from artifact (canonical + fallback).

    Canonical: artifact["references"]
    Fallback: Scan for FQDN-shaped strings ("::" pattern)

    Returns: Deduplicated list of reference FQDNs
    """
    refs = []

    # Canonical field
    if "references" in artifact:
        refs.extend(artifact["references"])

    # Fallback: Scan for FQDN-shaped values
    for key, value in artifact.items():
        if isinstance(value, str) and "::" in value:
            if value not in refs:
                refs.append(value)

    return refs
```

**Why Fallback?**
- Not all artifacts expose `references` field
- Some use nested fields (e.g., `core.dependencies`)
- Some derive references dynamically
- Future-safe for new artifact patterns

---

## Violation Schema

```json
{
  "artifact_fqdn": "pgs.platform.compiler::CT_BUILD_V0",
  "violation_code": "DANGLING_REFERENCE",
  "message": "Reference pgs.platform.compiler::CT_MISSING_V0 not found in compilation graph",
  "severity": "CRITICAL"
}
```

**Violation Codes**:
- `DANGLING_REFERENCE`: Reference not found in compilation graph
- `SHORT_NAME_REFERENCE`: Reference not using FQDN format (missing `::`)

---

## Execution Contract

**Preconditions**:
- Discovery complete (all artifacts discovered)
- Parse complete (all artifacts parsed to dict)
- Normalization complete (fqdn_id assigned to all artifacts)
- Validation complete (schema compliance verified)

**Postconditions**:
- If violations exist → Build fails with E701_ASSERTION_FAILURE
- If no violations → Build continues to materialization
- No side effects (no file writes, no state mutation)
- Deterministic (same input → same output)

**Performance**:
- O(N * M) where N = artifacts, M = avg references per artifact
- Expected: <100ms for typical platform build (~100 artifacts)

---

## Test Cases

### Test 1: Clean Graph (No Violations)

**Input**:
```python
artifacts_by_fqdn = {
    "pgs.platform.compiler::CT_A_V0": {
        "fqdn_id": "pgs.platform.compiler::CT_A_V0",
        "references": ["pgs.platform.compiler::CT_B_V0"]
    },
    "pgs.platform.compiler::CT_B_V0": {
        "fqdn_id": "pgs.platform.compiler::CT_B_V0",
        "references": []
    }
}
```

**Expected**: `violations = []` (build passes)

---

### Test 2: Dangling Reference

**Input**:
```python
artifacts_by_fqdn = {
    "pgs.platform.compiler::CT_A_V0": {
        "fqdn_id": "pgs.platform.compiler::CT_A_V0",
        "references": ["pgs.platform.compiler::CT_MISSING_V0"]  # Dangling!
    }
}
```

**Expected**:
```python
violations = [{
    "artifact_fqdn": "pgs.platform.compiler::CT_A_V0",
    "violation_code": "DANGLING_REFERENCE",
    "message": "Reference pgs.platform.compiler::CT_MISSING_V0 not found in compilation graph",
    "severity": "CRITICAL"
}]
```

**Build**: FAILS with E701_ASSERTION_FAILURE

---

### Test 3: Short Name Reference

**Input**:
```python
artifacts_by_fqdn = {
    "pgs.platform.compiler::CT_A_V0": {
        "fqdn_id": "pgs.platform.compiler::CT_A_V0",
        "references": ["CT_B_V0"]  # Short name!
    }
}
```

**Expected**:
```python
violations = [{
    "artifact_fqdn": "pgs.platform.compiler::CT_A_V0",
    "violation_code": "SHORT_NAME_REFERENCE",
    "message": "Reference CT_B_V0 not FQDN-normalized",
    "severity": "CRITICAL"
}]
```

**Build**: FAILS with E701_ASSERTION_FAILURE

---

## Version History

- **V0**: Initial implementation (2026-03-31) - ASSERT Activation Phase
