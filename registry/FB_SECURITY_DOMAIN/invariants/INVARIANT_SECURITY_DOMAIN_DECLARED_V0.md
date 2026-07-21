# INVARIANT_SECURITY_DOMAIN_DECLARED_V0

## Machine

```yaml
artifact_code: INVARIANT_SECURITY_DOMAIN_DECLARED_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0
fqdn: fb.security_domain::INVARIANT_SECURITY_DOMAIN_DECLARED_V0

core:
  summary: Every compiled snapshot must declare exactly one active security domain contract
  rule: >
    The compiler MUST locate exactly one active security domain contract within
    FB_SECURITY_DOMAIN. Zero contracts is a missing declaration violation.
    More than one active contract is an ambiguity violation.
  scope:
    - compiled_snapshot
  enforcement_stage:
    - compiler_validation
  violation_response: FAIL_COMPILE

# assert_projection — parameters the compiler-derived ASSERT carries (ASSERT is derived, not authored)
assert_projection:
  enforcement:
    phase: assert
    failure_mode: HARD_FAIL
    scope: ALL_ARTIFACTS
```

---

## Purpose

This invariant makes the V0 security domain contract load-bearing. It ensures that every
snapshot explicitly declares its information-control regime rather than leaving it undefined.
In V0, `UNCLASSIFIED_LOCAL` is not a default — it is a declared governance posture.
The difference matters: future classified execution modes require this axis to already exist
and be compiler-validated.

## Rule

For every compiled snapshot:
1. The compiler MUST scan `FB_SECURITY_DOMAIN/security_domain_contracts/` for active contracts
2. Exactly one MUST be present
3. The active contract's security domain MUST be materialized into `federation_profile.security_domain`
4. Compile MUST fail if no contract is found or more than one is found

## Anti-Patterns

- `no_security_domain_contract`: Snapshot compiled without any security domain contract present
- `multiple_active_contracts`: More than one security domain contract marked active simultaneously
- `visibility_declared_elsewhere`: Snapshot visibility declared in a non-security-domain boundary

## Enforcement

- **Stage:** compiler_validation
- **Failure Mode:** FAIL_COMPILE — no snapshot is produced if violated
