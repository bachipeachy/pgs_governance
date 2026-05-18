# INVARIANT_EV_APPEND_ONLY_V0

Architectural Invariant

## Machine

```yaml
invariant_code: INVARIANT_EV_APPEND_ONLY_V0
artifact_kind: INVARIANT
version: V0
governed_by: fb.constitution::CONSTITUTION_EVENT_V0

core:
  summary: EV artifacts must not declare mutation operations
  rule: EV artifacts must not contain update/delete/patch/mutate field declarations
  scope:
    - EV
```

## Summary

Event stores are append-only. EV artifact declarations must not express mutability semantics.
No field in an EV schema or extensions block may declare mutation intent.

## Rule

For every EV artifact:
1. `core.schema` MUST NOT contain mutation-signaling field names (`_update`, `_delete`, `_patch`, `_mutate`)
2. `extensions` MUST NOT declare mutation operation keys

Runtime append-only enforcement is provided by CS_APPENDONLY_JSONL_V0 and the execution engine.

## Enforcement Scope

- **Artifact Types**: EV
- **Validation Phase**: ASSERT (Phase 5, compile-time)
- **Runtime Enforcement**: CS_APPENDONLY_JSONL_V0 (hard fail at execution time)
- **Enforced By**: ASSERT_EV_APPEND_ONLY_V0

## Rationale

Append-only event stores are the foundation of auditability and replay. Mutation operations
on event records destroy the causal chain. This invariant ensures that no EV artifact
accidentally declares mutation semantics that could be interpreted as permitting mutation.
