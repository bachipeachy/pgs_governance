# ASSERT_SECURITY_DOMAIN_DECLARED_V0

## Machine

```yaml
artifact_code: ASSERT_SECURITY_DOMAIN_DECLARED_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.security_domain::INVARIANT_SECURITY_DOMAIN_DECLARED_V0

implementation:
  module: pgs_governance.registry.handlers.assert_security_domain_declared_v0
  callable: execute

enforcement:
  phase: assert
  failure_mode: HARD_FAIL
  scope: ALL_ARTIFACTS
```

---

## Summary

Validates that exactly one active security domain contract exists in `FB_SECURITY_DOMAIN`.

Enforces `INVARIANT_SECURITY_DOMAIN_DECLARED_V0`: every compiled snapshot must
declare active security domain semantics. Zero contracts is a missing declaration.
More than one active contract is an ambiguity violation.

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL
- **Scope**: All artifacts (scans `fb.security_domain` namespace)
