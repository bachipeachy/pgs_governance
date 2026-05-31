# ASSERT_RB_BINDING_POLICY_CONFORMANCE_V0

Architectural Assertion

## Machine

```yaml
artifact_code: ASSERT_RB_BINDING_POLICY_CONFORMANCE_V0
artifact_type: ASSERT
artifact_kind: ASSERT
version: 0

governed_by:
  - fb.topology::INVARIANT_RB_BINDING_POLICY_CONFORMANCE_V0

implementation:
  module: pgs_governance.registry.handlers.assert_rb_binding_policy_conformance_v0
  callable: execute
```

## Summary

Validates that every CS binding in an RB artifact declares an explicit `policy.path`
unless the CS type is `CS_MUTABLE_JSON_V0` (the only STRUCTURE-resolved CS type that
may use `policy: {}`).

An RB admitted to the snapshot with `policy: {}` for CS_REGISTRY_V0 or
CS_APPENDONLY_JSONL_V0 will crash at runtime initialization with a KeyError on
`policy['path']` — before any payload is processed, leaving an empty trace.
This assertion closes that compiler blind spot.

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All RB artifacts

## Handler Behavior

For every RB artifact, for every CS binding key in `core.bindings`:
1. Extract CS artifact code from the FQDN (segment after `::`)
2. If the CS code is `CS_MUTABLE_JSON_V0` → skip (STRUCTURE-resolved, `policy: {}` permitted)
3. Otherwise → `policy.path` must be declared and non-empty
4. `policy: {}` or missing/empty `policy.path` → VIOLATION

## Version History

- **V0**: Initial implementation — closes compiler blind spot where Compiler PASS → Runtime CRASH on empty RB policy
