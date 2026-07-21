# INVARIANT_EXECUTION_PLACEMENT_DECLARED_V0

## Machine

```yaml
artifact_code: INVARIANT_EXECUTION_PLACEMENT_DECLARED_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_INVARIANTS_V0
fqdn: fb.execution_placement::INVARIANT_EXECUTION_PLACEMENT_DECLARED_V0

core:
  summary: Every compiled snapshot must declare exactly one active execution placement contract
  rule: >
    The compiler MUST locate exactly one active placement contract within
    FB_EXECUTION_PLACEMENT. Zero contracts is a missing declaration violation.
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

This invariant is what makes the V0 placement contract non-dead-code. Without it, the
`STRUCTURE_EXECUTION_PLACEMENT_LOCAL_SINGLE_NODE_V0` would be documentation. With it, the compiler
is required to find and validate it — making placement declaration a hard compile-time
requirement, not an optional annotation.

## Rule

For every compiled snapshot:
1. The compiler MUST scan `FB_EXECUTION_PLACEMENT/placement_contracts/` for active contracts
2. Exactly one MUST be present
3. The active contract's placement mode MUST be materialized into `federation_profile.execution_placement`
4. Compile MUST fail if no contract is found or more than one is found

## Anti-Patterns

- `no_placement_contract`: Snapshot compiled without any placement contract present
- `multiple_active_contracts`: More than one placement contract marked active simultaneously
- `runtime_placement_override`: Runtime selecting placement mode at execution time

## Enforcement

- **Stage:** compiler_validation
- **Failure Mode:** FAIL_COMPILE — no snapshot is produced if violated
