# ASSERT_NO_SHORT_NAME_REFERENCE_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_NO_SHORT_NAME_REFERENCE_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.constitution::INVARIANT_NO_SHORT_NAME_REFERENCE_V0

implementation:
  module: pgs_governance.registry.handlers.assert_fqdn_only_references_v0
  callable: execute
```

## Summary

Validates all artifact references use FQDN format (no short names).

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All compiled artifacts

---

## Purpose

Enforce INVARIANT_NO_SHORT_NAME_REFERENCE_V0 during compilation.

**Execution Phase**: ASSERT (after VALIDATE, before MATERIALIZE)

**Failure Mode**: Build fails immediately on any violation (no warnings).
