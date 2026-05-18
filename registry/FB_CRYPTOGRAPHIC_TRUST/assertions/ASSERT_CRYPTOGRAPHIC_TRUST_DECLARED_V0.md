# ASSERT_CRYPTOGRAPHIC_TRUST_DECLARED_V0

## Machine

```yaml
artifact_code: ASSERT_CRYPTOGRAPHIC_TRUST_DECLARED_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.cryptographic_trust::INVARIANT_CRYPTOGRAPHIC_TRUST_DECLARED_V0

implementation:
  module: pgs_governance.registry.handlers.assert_cryptographic_trust_declared_v0
  callable: execute

enforcement:
  phase: assert
  failure_mode: HARD_FAIL
  scope: ALL_ARTIFACTS
```

---

## Summary

Validates that exactly one active trust contract exists in `FB_CRYPTOGRAPHIC_TRUST`.

Enforces `INVARIANT_CRYPTOGRAPHIC_TRUST_DECLARED_V0`: every compiled snapshot must
declare active cryptographic trust semantics. Zero contracts is a missing declaration.
More than one active contract is an ambiguity violation.

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL
- **Scope**: All artifacts (scans `fb.cryptographic_trust` namespace)
