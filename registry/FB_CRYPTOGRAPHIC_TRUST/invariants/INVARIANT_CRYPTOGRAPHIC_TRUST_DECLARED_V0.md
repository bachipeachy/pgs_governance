# INVARIANT_CRYPTOGRAPHIC_TRUST_DECLARED_V0

## Machine

```yaml
artifact_code: INVARIANT_CRYPTOGRAPHIC_TRUST_DECLARED_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0
fqdn: fb.cryptographic_trust::INVARIANT_CRYPTOGRAPHIC_TRUST_DECLARED_V0

core:
  summary: Every compiled snapshot must declare exactly one active cryptographic trust contract
  rule: >
    The compiler MUST locate exactly one active trust contract within
    FB_CRYPTOGRAPHIC_TRUST. Zero contracts is a missing declaration violation.
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

This invariant makes the V0 trust contract load-bearing. Trust posture is explicitly
declared for every snapshot — even in local unsigned development. The declaration
`LOCAL_DEV_UNSIGNED` is not an absence of trust governance; it is an explicit statement
that no cryptographic verification is required in this context. This sets up the
governance axis that future signed and attested execution modes will extend.

## Rule

For every compiled snapshot:
1. The compiler MUST scan `FB_CRYPTOGRAPHIC_TRUST/trust_contracts/` for active contracts
2. Exactly one MUST be present
3. The active contract's trust mode MUST be materialized into `federation_profile.cryptographic_trust`
4. Compile MUST fail if no contract is found or more than one is found

## Anti-Patterns

- `no_trust_contract`: Snapshot compiled without any trust contract present
- `multiple_active_contracts`: More than one trust contract marked active simultaneously
- `runtime_trust_negotiation`: Runtime selecting or upgrading trust mode at execution time

## Enforcement

- **Stage:** compiler_validation
- **Failure Mode:** FAIL_COMPILE — no snapshot is produced if violated
