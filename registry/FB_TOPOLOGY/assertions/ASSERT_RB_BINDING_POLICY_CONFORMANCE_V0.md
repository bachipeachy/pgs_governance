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
for CS types whose runtime implementations call `policy['path']` directly.

Currently all active CS types use STRUCTURE-based or entity-based resolution and permit
`policy: {}`:
- `CS_MUTABLE_JSON_V0`: STRUCTURE-based resolution via `storage_structure_artifact`
- `CS_APPENDONLY_JSONL_V0`: entity-based `__pgs_store_entity__` resolution
- `CS_REGISTRY_V0`: entity-based `__pgs_store_entity__` resolution (StorageUnavailable
  raised loudly if entity is unresolvable — not a silent KeyError)

This assertion is a forward guard: if a new CS type is introduced that calls
`policy['path']` directly, it must be added to `_FILE_PATH_CS_TYPES` in the handler.

## Enforcement

- **Phase**: 5 (ASSERT)
- **Failure Mode**: HARD FAIL (build stops)
- **Scope**: All RB artifacts

## Handler Behavior

For every RB artifact, for every CS binding key in `core.bindings`:
1. Extract CS artifact code from the FQDN (segment after `::`)
2. If the CS code is NOT in `_FILE_PATH_CS_TYPES` → skip (`policy: {}` permitted)
3. Otherwise → `policy.path` must be declared and non-empty
4. `policy: {}` or missing/empty `policy.path` → VIOLATION

## Version History

- **V0**: Initial implementation — closes compiler blind spot where Compiler PASS → Runtime CRASH on empty RB policy
- **V0 (updated)**: CS_REGISTRY_V0 migrated to entity-based resolution; removed from `_FILE_PATH_CS_TYPES`
