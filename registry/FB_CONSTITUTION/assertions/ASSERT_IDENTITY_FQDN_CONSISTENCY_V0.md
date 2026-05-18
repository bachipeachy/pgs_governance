# ASSERT_IDENTITY_FQDN_CONSISTENCY_V0

## Machine

```yaml
artifact_code: ASSERT_IDENTITY_FQDN_CONSISTENCY_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.constitution::INVARIANT_IDENTITY_FQDN_CONSISTENCY_V0

implementation:
  module: pgs_governance.registry.handlers.assert_identity_fqdn_consistency
  callable: execute

enforcement:
  phase: validation
  order: 5
  failure_mode: HARD_FAIL
  scope: ALL_ARTIFACTS
```

---

## Summary

Validates FQDN matches namespace and artifact_code consistently.

FQDN format: `{namespace}::{artifact_code}`

---

## Enforcement

- **Phase**: Validation (during compilation)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All artifacts

---

## Validation Rules

### Rule 1: FQDN Structure
FQDN must contain exactly one `::` separator.

### Rule 2: FQDN Parts
FQDN splits into exactly 2 parts: namespace and code.

### Rule 3: Namespace Match
FQDN namespace part must match artifact's actual namespace.

### Rule 4: Code Match
FQDN code part must match artifact's declared artifact_code.

---

## Error Messages

### FQDN Mismatch
```
❌ ASSERT_IDENTITY_FQDN_CONSISTENCY_V0: FQDN inconsistency

Artifact: CT_PURE_VALIDATE_V0
Declared FQDN: transforms::CT_PURE_VALIDATE_V0
Expected FQDN: capability_transforms::CT_PURE_VALIDATE_V0

Violation: Namespace mismatch
Fix: Update FQDN to match actual namespace
```

---

## Version History

- **V0**: Initial implementation (2026-04-06) - Identity Consistency Enforcement
- **V0.1**: Updated schema (2026-04-12) - Added Machine section
